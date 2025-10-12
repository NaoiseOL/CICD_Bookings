from fastapi import FastAPI, HTTPException, status
from .schemas import User
from .schemas import Booking_Info

app = FastAPI()
users: list[User] = []
bookings: list[Booking_Info] = []

#Code for Users operations

@app.get("/api/users")
def get_users():
    return users

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    for u in users:
        if u.user_id == user_id:
            return u
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    if any(u.user_id == user.user_id for u in users):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user_id already exists")
    users.append(user)
    return user

@app.put("/api/users/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: int, new_user: User):
    for i, u in enumerate(users):
        if u.user_id == user_id:
            users[i] = new_user
            return new_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.user_id == user_id:
            users.pop(i)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )

#Code for booking operations

@app.get("/api/booking")
def get_bookings():
    return bookings

@app.get("/api/booking/{booking_id}")
def get_booking(booking_id: int):
    for b in bookings:
        if b.booking_id == booking_id:
            return b
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

@app.post("/api/bookings", status_code=status.HTTP_201_CREATED)
def add_booking(booking: Booking_Info):
    if any(b.booking_id == booking.booking_id for b in bookings):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="booking_id already exists")
    bookings.append(booking)
    return booking

@app.put("/api/bookings/{booking_id}", status_code=status.HTTP_200_OK)
def update_booking(booking_id: int, new_booking: Booking_Info):
    for i, b in enumerate(bookings):
        if b.booking_id == booking_id:
            bookings[i] = new_booking
            return new_booking
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

@app.delete("/api/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(booking_id: int):
    for i, b in enumerate(bookings):
        if b.booking_id == booking_id:
            bookings.pop(i)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")