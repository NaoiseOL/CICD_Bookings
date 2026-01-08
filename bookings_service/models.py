from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey


class Base(DeclarativeBase):
    pass

class BookingsDB(Base):
    __tablename__ = "bookings"
    booking_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    start_Date: Mapped[str] = mapped_column(String(100), nullable=False)
    end_Date: Mapped[str] = mapped_column(String(100), nullable=False)