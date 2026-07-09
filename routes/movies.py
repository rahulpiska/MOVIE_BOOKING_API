from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Movie, Show
from schemas import MovieCreate,MovieUpdate,MovieResponse,ShowResponse
from utils import get_current_admin
from sqlalchemy import func

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)

@router.post("", response_model=MovieResponse)
def create_movie(movie:MovieCreate,
                 current_user: User = Depends(get_current_admin),
                 db:Session = Depends(get_db)):
    
    existing_movie = (
        db.query(Movie).filter(
        func.lower(Movie.title) == movie.title.lower())
        .first()
    )


    if existing_movie:
        raise HTTPException(
            status_code=400,
            detail="Movie with this title already exists"
        )
    
    
    add_movie = Movie(
        title= movie.title,
        description= movie.description,
        language= movie.language,
        genre= movie.genre,
        duration_minutes= movie.duration_minutes,
        release_date= movie.release_date
    )

    db.add(add_movie)
    db.commit()
    db.refresh(add_movie)

    return add_movie

#------------------------------------------------------------------

@router.get("", response_model=list[MovieResponse])
def get_movies(db:Session = Depends(get_db)):

    movies = db.query(Movie).all()

    return movies

#-------------------------------------------------------------------

@router.get("/{id}", response_model=MovieResponse)
def get_movie_by_id(id: int,
                    db:Session = Depends(get_db)):

    movie = db.query(Movie).filter(Movie.id == id).first()

    if not movie:
        raise HTTPException(
        status_code=404,
        detail="Movie not found"
    )

    return movie

#-------------------------------------------------------------------

@router.get("/{movie_id}/shows", response_model=list[ShowResponse])
def get_shows_of_movie(movie_id: int,
                       db:Session = Depends(get_db)):
    
    movie = (
        db.query(Movie)
        .filter(Movie.id == movie_id)
        .first()
    )

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )
    
    shows = (
        db.query(Show)
        .filter(Show.movie_id == movie.id)
        .all()
    )

    if not shows:
        raise HTTPException(
            status_code=404,
            detail="Movie has no shows"
        )
    
    return shows

#-------------------------------------------------------------------

@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int,
                update: MovieUpdate,
                current_user:User = Depends(get_current_admin),
                db:Session = Depends(get_db)):
    
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )
    
    if update.title is not None:

        existing_movie = (
            db.query(Movie)
            .filter(
                func.lower(Movie.title) == update.title.lower(),
                Movie.id != movie.id
            )
            .first() 
        )

        if existing_movie:
            raise HTTPException(
                status_code=400,
                detail="Movie title already exists"
            )
        
        movie.title = update.title

    if update.description is not None:
        movie.description = update.description

    if update.language is not None:
        movie.language = update.language

    if update.genre is not None:
        movie.genre = update.genre

    if update.duration_minutes is not None:
        movie.duration_minutes = update.duration_minutes

    if update.release_date is not None:
        movie.release_date = update.release_date

    db.commit()
    db.refresh(movie)

    return movie

#------------------------------------------------------------------

@router.delete("/{id}")
def delete_movie(id: int,
                 current_user:User = Depends(get_current_admin),
                 db:Session = Depends(get_db)):
    
    movie = db.query(Movie).filter(Movie.id == id).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )
    
    if movie.shows:
        raise HTTPException(
            status_code=400,
            detail="Movie has shows"
        )
    
    db.delete(movie)
    db.commit()
    
    return (
        {"message":"Movie deleted successfully"}
    )
        
    

    