from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .database import engine, SessionLocal
from .models import Base, BookingsDB
from .schemas import BookingCreate, BookingRead, BookingUpdate
from .rabbit import publish_event
import asyncio
import os
import json

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/bookings", response_model=list[BookingRead])
def list_bookings(db: Session = Depends(get_db)):
    stmt = select(BookingsDB).order_by(BookingsDB.booking_id)
    result = db.execute(stmt)
    bookings = result.scalars().all()
    return bookings


@app.get("/api/bookings/{booking_id}", response_model=BookingRead)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.get(BookingsDB, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Boooking not found")
    return booking


@app.post("/api/bookings", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
async def add_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    booking = BookingsDB(**payload.dict(exclude_unset=True))
    db.add(booking)
    try:
        db.commit()
        db.refresh(booking)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Booking already exists")
    
    asyncio.create_task(
        publish_event(
            "booking.created",
            {
                "user_id": booking.user_id,
                "first_name": booking.first_name,
                "surname": booking.surname,
                "start_date": booking.start_Date,
                "end_date": booking.end_Date
            }
        )
    )
    return booking

@app.put("/api/bookings/{booking_id}", response_model=BookingRead)
async def replace_booking(booking_id: int, payload: BookingCreate, db: Session = Depends(get_db)):
    booking = db.get(BookingsDB, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="booking not found")

    booking.user_id = payload.user_id
    booking.first_name = payload.first_name
    booking.surname = payload.surname
    booking.start_Date = payload.start_Date
    booking.end_Date = payload.end_Date

    try:
        db.commit()
        db.refresh(booking)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Booking update Failed")
    
    asyncio.create_task(
        publish_event(
            "booking.updated",
            {
                "user_id": booking.user_id,
                "first_name": booking.first_name,
                "surname": booking.surname,
                "start_date": booking.start_Date,
                "end_date": booking.end_Date
            }
        )
    )

    return booking

@app.delete("/api/bookings/{booking_id}", status_code=204)
async def delete_booking(booking_id: int, db: Session = Depends(get_db)) -> Response:
    booking = db.get(BookingsDB, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="booking not found")

    asyncio.create_task(
        publish_event(
            "booking.deleted",
            {
                "user_id" : booking.user_id,
                "first_name" : booking.first_name,
                "surname" : booking.surname,
                "start_date" : booking.start_Date,
                "end_date" : booking.end_Date
            }
        )
    )

    db.delete(booking)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/api/bookings/{booking_id}", response_model=BookingRead)
async def patch_booking(booking_id: int, payload: BookingUpdate, db: Session = Depends(get_db)):
    booking = db.get(BookingsDB, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking Not Found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(booking, field, value)

    try:
        db.commit()
        db.refresh(booking)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Booking Patch Failed")

    asyncio.create_task(
        publish_event(
            "booking.patched",
            {
                "user_id" : booking.user_id,
                "first_name" : booking.first_name,
                "surname" : booking.surname,
                "start_date" : booking.start_Date,
                "end_date" : booking.end_Date
            }
        )
    )

    return booking