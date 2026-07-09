from sqlalchemy import (String, Column,DateTime,
                        Integer,Boolean,TEXT,func, Date, ForeignKey,
                        Numeric, UniqueConstraint, Enum)
from sqlalchemy.orm import relationship
from database import Base

from enum import Enum as pyEnum


class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(225), unique=True, index=True,nullable=False)
    password = Column(String(225),nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime,server_default=func.now())

    bookings = relationship( 
        "Booking",
        back_populates= "user",
        cascade="all, delete-orphan"
    )
#--------------------------------------------------------------------------

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True, unique=True,nullable=False)
    description = Column(TEXT,nullable=False)
    language = Column(String(50), nullable=False)
    genre = Column(String(200),nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    shows = relationship(
        "Show",
        back_populates="movie",
        cascade="all, delete-orphan"
    ) 
#---------------------------------------------------------------------------

class Theater(Base):
    __tablename__ = "theaters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True,nullable=False, index=True)

    screens = relationship(
        "Screen",
        back_populates="theater",
        cascade="all, delete-orphan"
    )
#--------------------------------------------------------------------------

class Screen(Base):
    __tablename__ = "screens"

    __table_args__ = (
        UniqueConstraint(
            "theater_id",
            "name",
            name="unique_screen_per_theater"
        ),
    )

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String(10), nullable=False)
    theater_id = Column(Integer, ForeignKey("theaters.id"), nullable=False)

    theater = relationship(
        "Theater",
        back_populates= "screens"
    )

    shows = relationship(
        "Show",
        back_populates= "screen",
        cascade="all, delete-orphan"
    )

    seats = relationship(
        "Seat",
        back_populates= "screen",
        cascade="all, delete-orphan"
    )
#--------------------------------------------------------------------------

class Show(Base):
    __tablename__ = "shows"

    __table_args__ = (
        UniqueConstraint(
            "screen_id",
            "start_time",
            name="unique_show_per_screen_time"
        ),
    )

    id = Column(Integer, primary_key=True,index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    screen_id = Column(Integer, ForeignKey("screens.id"), nullable=False, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    ticket_price = Column(Numeric(10,2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


    movie = relationship(
        "Movie",
        back_populates= "shows"
    )

    screen = relationship(
        "Screen",
        back_populates= "shows"
    )

    bookings = relationship(
        "Booking",
        back_populates="show"
    )

    booking_seats = relationship(
        "BookingSeat",
        back_populates= "show",
        cascade="all, delete-orphan"
    )

#---------------------------------------------------------------------------
    
class Seat(Base):
    __tablename__ = "seats"

    __table_args__ = (
        UniqueConstraint(
            "screen_id",
            "seat_number",
            name="unique_seat_per_screen"
        ),
    )

    id = Column(Integer, primary_key=True, index=True )
    screen_id = Column(Integer, ForeignKey("screens.id"), index=True, nullable=False)
    seat_number = Column(String(5),nullable=False)

    screen = relationship(
        "Screen",
        back_populates= "seats"
    )

    booking_seats = relationship(
        "BookingSeat",
        back_populates= "seat"
    )
#--------------------------------------------------------------------------
class BookingStatus(str, pyEnum):
        PENDING = "Pending"
        CONFIRMED = "Confirmed"
        CANCELLED = "Cancelled"


class Booking(Base):
    __tablename__ = "bookings"



    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"),index=True, nullable=False)
    show_id = Column(Integer, ForeignKey("shows.id"), index=True, nullable=False)
    total_amount = Column(Numeric(10,2), nullable=False)
    status = Column(Enum(BookingStatus), nullable=False, default=BookingStatus.CONFIRMED)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship(
        "User",
        back_populates= "bookings" 
    )

    show = relationship(
        "Show",
        back_populates= "bookings"
    )

    booking_seats = relationship(
        "BookingSeat",
        back_populates= "booking"
    )


#--------------------------------------------------------------------------

class BookingSeat(Base):
    __tablename__ = "booking_seats"

    __table_args__ = (
        UniqueConstraint(
        "show_id",
        "seat_id",
        name="unique_seat_per_show"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    show_id = Column(Integer, ForeignKey("shows.id"), nullable=False, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False, index=True)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False, index=True)
    price = Column(Numeric(10,2), nullable=False)

    booking = relationship(
        "Booking",
        back_populates= "booking_seats"
    )

    seat = relationship(
        "Seat",
        back_populates= "booking_seats"
    )

    show = relationship(
        "Show",
        back_populates= "booking_seats"
    )





#===============================================================================