from database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends
from models import User
from schemas import UserCreate, UserResponse
from utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("", response_model=UserResponse)
def create_user(user: UserCreate,
                db:Session = Depends(get_db)):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    
    hashed_password = hash_password(user.password)

    
    new_user = User(
        name = user.name,
        email = user.email,
        password = hashed_password
    )

    db.add(new_user)

    db.commit()
    db.refresh(new_user)

    return new_user
