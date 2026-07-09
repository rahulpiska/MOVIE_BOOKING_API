from database import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User
from schemas import UserResponse
from utils import get_current_user, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login")
def user_login(form_data: OAuth2PasswordRequestForm = Depends(),
               db:Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credintials"
        )
    
    password_valid = verify_password(
        form_data.password,
        user.password
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid credintials"
        )
    
    token = create_access_token(
        {"user_id": user.id}
    )
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }

#----------------------------------------------------------------------------------

@router.get("/me",response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):

    return current_user