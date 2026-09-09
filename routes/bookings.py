from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from utils import get_current_user, get_current_admin
from models import User, Show, Seat, BookingSeat, Booking, BookingStatus
from schemas import BookingCreate, BookingResponse, BookingDetailsResponse
from datetime import datetime

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

@router.post("",response_model=BookingResponse)
def create_booking(create:BookingCreate,
                   current_user:User = Depends(get_current_user),
                   db:Session = Depends(get_db)):
    
    show = (
        db.query(Show)
        .filter(Show.id == create.show_id)
        .first()
    )
    if not show:
        raise HTTPException(
            status_code=404,
            detail="Show not available"
        )
    
    seats = (
        db.query(Seat)
        .filter(
            Seat.id.in_(create.seat_ids),
            Seat.screen_id == show.screen_id
        )
        .all()
    )

    if len(seats) != len(create.seat_ids):
        raise HTTPException(
            status_code=400,
            detail="Invalid seats"
        )
    
    booking_seats = (
        db.query(BookingSeat)
        .join(Booking, Booking.id == BookingSeat.booking_id)
        .filter(
            BookingSeat.show_id == show.id,
            BookingSeat.seat_id.in_(create.seat_ids),
            Booking.status == BookingStatus.CONFIRMED
        )
        .all()
    )

    booked_seat_ids = {
        booking.seat_id
        for booking in booking_seats
    }

    for seat in seats:
        if seat.id in booked_seat_ids:
            raise HTTPException(
                status_code=400,
                detail="Seats unavailable"
            )
        

    new_book = Booking(
        user_id = current_user.id,
        show_id = show.id,
        total_amount = show.ticket_price * len(create.seat_ids)

    )

    try:
        db.add(new_book)
        db.flush()

        for seat_id in create.seat_ids:
            booking_seat = BookingSeat(
                show_id = show.id,
                booking_id = new_book.id,
                seat_id = seat_id,
                price = show.ticket_price
            )

            db.add(booking_seat)

        db.commit()
        db.refresh(new_book)

        return new_book

    except:
        db.rollback()
        raise 

#----------------------------------------------------------------------------

@router.get("", response_model=list[BookingResponse])
def get_bookings(current_user:User = Depends(get_current_user),
                 db:Session = Depends(get_db)):
    
    bookings = (
        db.query(Booking)
        .filter(Booking.user_id == current_user.id)
    )
    
    return bookings

#-----------------------------------------------------------------------------

@router.get("/{booking_id}",response_model=BookingDetailsResponse)
def get_booking_details(booking_id: int,
                        current_user:User = Depends(get_current_user),
                        db:Session = Depends(get_db)):
    
    booking = (
        db.query(Booking)
        .filter(
            Booking.id == booking_id,
            Booking.user_id == current_user.id
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking Details not found"
        )
    
    seat_numbers = []

    for booking_seat in booking.booking_seats:
        seat_numbers.append(
            booking_seat.seat.seat_number
        )
    
    return {
        "booking_id": booking.id,
        "movie": booking.show.movie.title,
        "theater": booking.show.screen.theater.name,
        "screen": booking.show.screen.name,
        "start_time": booking.show.start_time,
        "status": booking.status,
        "total_amount": booking.total_amount,
        "seats": seat_numbers
    }

#---------------------------------------------------------------------------

@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
def update_status(booking_id: int,
                  current_user: User = Depends(get_current_user),
                  db:Session = Depends(get_db)):
    
    booking = (
        db.query(Booking)
        .filter(
            Booking.id == booking_id,
            Booking.user_id == current_user.id
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )
    
    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(
            status_code=400,
            detail="Booking already Cancelled"
        )
    
    if booking.show.start_time <= datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel after the show has started"
        )
    
    booking.status = BookingStatus.CANCELLED

    db.commit()
    db.refresh(booking)

    return booking
    