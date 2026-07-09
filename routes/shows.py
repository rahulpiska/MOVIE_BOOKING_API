from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from models import Movie, Screen, Show, User, Seat,BookingSeat
from utils import get_current_admin
from schemas import ShowCreate, ShowResponse, ShowUpdate
from datetime import  timedelta

router = APIRouter(
    prefix="/shows",
    tags=["Shows"]
)

@router.post("",response_model=ShowResponse)
def create_show(add_show:ShowCreate,
                current_user:User = Depends(get_current_admin),
                db:Session = Depends(get_db)):
    
    movie = (
        db.query(Movie)
        .filter(Movie.id == add_show.movie_id)
        .first()
    )
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )
    
    screen = (
         db.query(Screen)
         .filter(Screen.id == add_show.screen_id)
         .first()
    )

    if not screen:
        raise HTTPException(
            status_code=404,
            detail="Screen not found"
        )
    
    end_time = add_show.start_time + timedelta(minutes=movie.duration_minutes)


    check_time = (
        db.query(Show)
        .filter(
            Show.screen_id == add_show.screen_id,
            Show.start_time < end_time,
            Show.end_time > add_show.start_time
        )
        .first()
    )

    if check_time:
        raise HTTPException(
            status_code=400,
            detail="This show overlaps with an existing show on this screen"
        )
    
    new_show = Show(
        movie_id = add_show.movie_id,
        screen_id = add_show.screen_id,
        start_time = add_show.start_time,
        end_time = end_time,
        ticket_price = add_show.ticket_price
    )


    db.add(new_show)
    db.commit()
    db.refresh(new_show)

    return new_show

#-----------------------------------------------------------------------

@router.get("",response_model=list[ShowResponse])
def get_shows(db:Session = Depends(get_db)):

    shows = db.query(Show).all()

    return shows

#-------------------------------------------------------------------
@router.get("/{show_id}",response_model=ShowResponse)
def get_show_by_id(show_id: int,
                   db:Session = Depends(get_db)):
    
    show = (
        db.query(Show)
        .filter(Show.id == show_id)
        .first()
    )

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )
    
    return show

#--------------------------------------------------------------------

@router.get("/{show_id}/seats")
def seats_for_show(show_id: int,
                   db:Session = Depends(get_db)):
    
    show = (
        db.query(Show)
        .filter(Show.id == show_id)
        .first()
    )
    if not show:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )
    
    seats = (
        db.query(Seat)
        .filter(Seat.screen_id == show.screen_id)
        .all()
    )
    
    booking_seats = (
        db.query(BookingSeat)
        .filter(BookingSeat.show_id == show.id)
        .all()
    )

    booked_seat_ids = {
        booking.seat_id
        for booking in booking_seats
    }

    response = []

    for seat in seats:
        response.append(
            {
                "seat_id":seat.id,
                "Seat_number":seat.seat_number,
                "available":seat.id not in booked_seat_ids
            }
        )
    
    return response

#---------------------------------------------------------------------

@router.put("/{show_id}", response_model=ShowResponse)
def update_show(show_id: int,
                update:ShowUpdate,
                current_user: User = Depends(get_current_admin),
                db:Session = Depends(get_db)):
    
    show = (
        db.query(Show)
        .filter(Show.id == show_id)
        .first()
    )

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )
    
    movie_id = update.movie_id or show.movie_id

    movie =(
        db.query(Movie)
        .filter(Movie.id == movie_id)
        .first()
    )
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )


    start_time = update.start_time or show.start_time
    end_time = start_time + timedelta(minutes=movie.duration_minutes)
    screen_id = update.screen_id or show.screen_id
    ticket_price = update.ticket_price or show.ticket_price

    screen = (
        db.query(Screen)
        .filter(Screen.id == screen_id)
        .first()
    )
    if not screen:
        raise HTTPException(
            status_code=404,
            detail="Screen not found"
        )

    existing_screen = (
        db.query(Show)
        .filter(
            Show.screen_id == screen.id,
            Show.start_time < end_time,
            Show.end_time > start_time,
            Show.id != show.id
            )
        .first()
    )

    if existing_screen:
        raise HTTPException(
            status_code=400,
            detail="This show overlaps with an existing show on this screen"
        )
    

    show.movie_id = movie.id
    show.screen_id = screen.id
    show.start_time = start_time
    show.end_time = end_time
    show.ticket_price = ticket_price


    db.commit()
    db.refresh(show)

    return show

#---------------------------------------------------------------------

@router.delete("/{show_id}")
def delete_show(show_id: int,
                current_user:User = Depends(get_current_admin),
                db:Session = Depends(get_db)):
    
    show = (
        db.query(Show)
        .filter(Show.id == show_id)
        .first()
    )

    if not show:
        raise HTTPException(
            status_code=404,
            detail="Show not found"
        )
    
    if show.bookings:
        raise HTTPException(
            status_code=400,
            detail="Show has bookings"
        )
    
    db.delete(show)
    db.commit()

    return (
        {"message":"Show deleted successfully"}
    )