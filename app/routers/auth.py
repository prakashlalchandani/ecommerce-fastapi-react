from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import user as models
from utils import Hash, create_access_token
from schemas import user as schemas

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm returns username and password
    # in our model we use email as the identifier to login (usually)
    # verify.py had username=Column(String, unique=True, index=True) and email=Column(String, unique=True, index=True)
    # The user request said "Users can login with username and password".
    # oauth2.py implementation I wrote checked email. 
    # Let's verify what the users.py does. 
    # users.py: db_user = User(email=user.email, username=user.username, password=user.password)
    # So both exist.
    # The OAuth2 spec says "username" field.
    # I will stick to checking the 'username' column OR 'email' column? 
    # Usually OAuth2PasswordRequestForm puts the login identifier in 'username'.
    # I'll check against the User.email field as that is often unique and standard, but the prompt said "username and password".
    # However, standard practice with OAuth2PasswordRequestForm is to use the `username` attribute for the identifier.
    # Let's check `d:/Projects/e-commerce/app/models/user.py` content again.
    # 9:     username = Column(String, unique=True, index=True)
    # 10:    email = Column(String, unique=True, index=True)
    # I will query against the `email` column using `user_credentials.username` as the value, 
    # OR I could query against `username`. 
    # The prompt said: "Users can login with username and password".
    # I will implementation login via *email* as it is more robust, but I should probably support what the user expects.
    # But wait, in `oauth2.py` I wrote: `user = db.query(models.User).filter(models.User.email == username).first()`
    # So I should be consistent. If I use email in token (subject), I should login with email.
    
    # Support login with either Username or Email
    # We check if the provided credential matches either the email or the username column
    from sqlalchemy import or_
    user = db.query(models.User).filter(
        or_(
            models.User.email == user_credentials.username,
            models.User.username == user_credentials.username
        )
    ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not Hash.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # Generate Token
    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "role": user.role
    }
