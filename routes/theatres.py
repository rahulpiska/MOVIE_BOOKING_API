from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from utils import get_current_admin
from sqlalchemy import func
from models import Theater,User
from schemas import TheaterCreate, TheaterResponse, TheaterUpdate


router= APIRouter(
    prefix="/theaters",
    tags=["Theaters"]
)

@router.post("",response_model=TheaterResponse)
def create_theater(theater:TheaterCreate,
                   current_user: User = Depends(get_current_admin),
                   db:Session = Depends(get_db)):
    
    existing_theater = (
        db.query(Theater).filter(
            func.lower(Theater.name) == theater.name.lower())
            .first()
        )
    if existing_theater:
        raise HTTPException(
            status_code=400,
            detail="Theater already exists with this name"
        )
    
    new_theater = Theater(
        name=theater.name
    )

    db.add(new_theater)
    db.commit()
    db.refresh(new_theater)

    return new_theater

#--------------------------------------------------------------------

@router.get("",response_model=list[TheaterResponse])
def get_theaters(db:Session = Depends(get_db)):

    theaters = db.query(Theater).all()

    return theaters

#----------------------------------------------------------------------

@router.get("/{id}", response_model=TheaterResponse)
def get_theater_by_id(id: int,
                      db:Session = Depends(get_db)):
    
    theater = db.query(Theater).filter(Theater.id == id).first()

    if not theater:
        raise HTTPException(
            status_code=404,
            detail="Theater not found"
        )
    
    return theater

#------------------------------------------------------------------

@router.put("/{theater_id}", response_model=TheaterResponse)
def update_theater(theater_id:int,
                   update: TheaterUpdate,
                   current_user: User = Depends(get_current_admin),
                   db:Session = Depends(get_db)):
    
    theater =(
         db.query(Theater)
         .filter(Theater.id == theater_id)
         .first()
    )

    if not theater:
        raise HTTPException(
            status_code=404,
            detail="Theater not found"
        )
    
    
    if update.name is not None:

        existing_theater = (
            db.query(Theater)
            .filter(
                func.lower(Theater.name) == update.name.lower(),
                Theater.id != theater.id
            )
            .first()
        )

        if existing_theater:
            raise HTTPException(
                status_code=400,
                detail="Theater with this name already exists"
            )
    
        theater.name = update.name

    db.commit()
    db.refresh(theater)

    return theater

#--------------------------------------------------------------------

@router.delete("/{theater_id}")
def delete_theater(theater_id: int,
                   current_user: User = Depends(get_current_admin),
                   db:Session = Depends(get_db)):
    
    theater = (
        db.query(Theater)
        .filter(Theater.id == theater_id)
        .first()
    )

    if not theater:
        raise HTTPException(
            status_code=404,
            detail="Theater not found"
        )
    
    if theater.screens:
        raise HTTPException(
            status_code=400,
            detail="theater has screens"
        )
    
    db.delete(theater)
    db.commit()

    return (
        {"message":"Theater deleted successfully"}
    )


