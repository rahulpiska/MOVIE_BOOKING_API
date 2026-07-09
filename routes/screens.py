from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Theater, Screen, Seat
from utils import get_current_admin
from schemas import ScreenCreate, ScreenResponse, ScreenUpdate
from sqlalchemy import func

router = APIRouter(
    prefix="/screens",
    tags=["Screens"]
)

@router.post("", response_model=ScreenResponse)
def create_screen(add_screen:ScreenCreate,
                  current_user:User = Depends(get_current_admin),
                  db:Session = Depends(get_db)):
    
    theater = (
        db.query(Theater)
        .filter(Theater.id == add_screen.theater_id)
        .first()
    )

    if not theater:
        raise HTTPException(
            status_code=400,
            detail="Invalid theater id"
        )
    
    existing_screen = (
        db.query(Screen)
        .filter(
            Screen.theater_id == add_screen.theater_id,
            func.lower(Screen.name) == add_screen.name.lower()
        )
        .first()
    )
    
    if existing_screen:
        raise HTTPException(
            status_code=400,
            detail="Screen with this name already exists"
        )
    
    new_screen = Screen(
        name = add_screen.name,
        theater_id = add_screen.theater_id
    )
    
    db.add(new_screen)
    db.flush()

    rows = add_screen.rows
    cols = add_screen.seats_per_row

    seats = []

    for row in range(rows):
        row_letter = chr(65 + row)
        for col in range(1, cols + 1):
            seats.append(
                Seat(
                    screen_id = new_screen.id,
                    seat_number = f"{row_letter}{col}"
                )
            )


    db.add_all(seats)
    db.commit()
    db.refresh(new_screen)
    
    return new_screen

#--------------------------------------------------------------------------

@router.get("",response_model=list[ScreenResponse])
def get_screens(db:Session = Depends(get_db)):

    screens = db.query(Screen).all()

    return screens

#---------------------------------------------------------------------

@router.get("/{screen_id}", response_model=ScreenResponse)
def get_screens_by_id(screen_id: int,
                      db:Session = Depends(get_db)):
    

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
    
    return screen

#---------------------------------------------------------------------

@router.put("/{screen_id}", response_model=ScreenResponse)
def get_screen_by_id(screen_id: int,
                     update:ScreenUpdate,
                     current_user:User = Depends(get_current_admin),
                     db:Session = Depends(get_db)):
    
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
    
    if update.theater_id is not None:

        theater = (
            db.query(Theater)
            .filter(Theater.id == update.theater_id)
            .first()
        )

        if not theater:
            raise HTTPException(
                status_code=404,
                detail="Theater not found"
            )

    
    theater_id = update.theater_id or screen.theater_id
    name = update.name or screen.name

    existing_screen = (
        db.query(Screen)
        .filter(
            func.lower(Screen.name) == name.lower(),
            Screen.theater_id == theater_id,
            Screen.id != screen.id
        )
        .first()
    )

    if existing_screen:
        raise HTTPException(
            status_code=400,
            detail="Theater already exists with this screen name"
        )
        
    screen.name = name
    screen.theater_id = theater_id
        
    db.commit()
    db.refresh(screen)

    return screen
#----------------------------------------------------------------------

@router.delete("/{screen_id}")
def delete_screen(screen_id: int,
                  curren_user:User = Depends(get_current_admin),
                  db:Session = Depends(get_db)):
    
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
    
    if screen.shows:
        raise HTTPException(
            status_code=400,
            detail="Screen has shows"
        )
    
    db.delete(screen)
    db.commit()

    return (
        {"message":"Screen deleted successfully"}
    )

