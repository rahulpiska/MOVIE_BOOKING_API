from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime, date
from decimal import Decimal
from models import BookingStatus

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
    created_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True
    )

#-----------------------------------------------------------

class MovieCreate(BaseModel):
    title: str
    description: str
    language: str
    genre: str
    duration_minutes: int = Field(gt=0)
    release_date: date 

class MovieUpdate(BaseModel):
    title: str | None= None
    description: str | None= None
    language: str | None= None
    genre: str | None= None
    duration_minutes: int | None = Field(default=None, gt=0)
    release_date: date | None= None
    
class MovieResponse(BaseModel):
    id: int
    title: str
    description: str
    language: str
    genre: str
    duration_minutes: int= Field(gt=0)
    release_date: date 
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
    
#-----------------------------------------------------

class TheaterCreate(BaseModel):
    name: str

class TheaterUpdate(BaseModel):
    name: str

class TheaterResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )

#----------------------------------------------------

class ScreenCreate(BaseModel):
    name: str
    theater_id: int
    rows: int= Field(gt=0)
    seats_per_row: int= Field(gt=0)

class ScreenUpdate(BaseModel):
    name: str | None= None
    theater_id: int | None= None

class ScreenResponse(BaseModel):
    id: int
    name: str
    theater_id: int

    model_config = ConfigDict(
        from_attributes=True
    )

#-----------------------------------------------------

class ShowCreate(BaseModel):
    movie_id: int
    screen_id: int
    start_time: datetime
    ticket_price: Decimal= Field(gt=0)

class ShowUpdate(BaseModel):
    movie_id: int | None= None
    screen_id: int | None= None
    start_time: datetime | None= None
    ticket_price: Decimal | None = Field(default=None, gt=0)

class ShowResponse(BaseModel):
    id: int
    movie_id: int
    screen_id: int
    start_time: datetime
    end_time: datetime
    ticket_price: Decimal = Field(gt=0)
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

#-----------------------------------------------------------

class SeatsResponse(BaseModel):
    id: int
    screen_id: int
    seat_number: str

    model_config = ConfigDict(
        from_attributes=True
    )

class SeatsForShow(BaseModel):
    seat_id: int
    seat_number: str
    available: bool

    model_config = ConfigDict(
        from_attributes=True
    )

#--------------------------------------------------------

class BookingCreate(BaseModel):
    show_id: int = Field(gt=0)
    seat_ids: list[int]


class BookingResponse(BaseModel):
    id: int
    show_id: int
    total_amount: Decimal
    status: BookingStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

#---------------------------------------------

class BookingDetailsResponse(BaseModel):
    booking_id: int
    movie: str
    theater: str
    screen: str
    start_time: datetime
    status: BookingStatus
    total_amount: Decimal
    seats: list[str]

    model_config = ConfigDict(
        from_attributes=True
    )

