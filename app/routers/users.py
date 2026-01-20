from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User  # <--- You already imported User here
from schemas.user import UserCreate, User as UserSchema
from utils import Hash
import oauth2  # <--- 1. ADD THIS IMPORT

router = APIRouter()

@router.post("/users", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = Hash.bcrypt(user.password)
    
    db_user = User(
        email=user.email, 
        username=user.username, 
        password=hashed_password,
        role=user.role 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# GET /users/me
@router.get("/users/me", response_model=UserSchema)
def read_users_me(
    current_user: User = Depends(oauth2.get_current_user) # <--- 2. CHANGED 'models.User' to 'User'
):
    return current_user