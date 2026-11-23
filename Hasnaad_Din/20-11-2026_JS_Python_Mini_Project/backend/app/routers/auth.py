# routers/auth.py - signup, login (username OR email), login with Google, who am I
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.config import GOOGLE_CLIENT_ID
from app.database import get_db
from app.models import User
from app.schemas import GoogleLogin, Token, UserCreate, UserRead
from app.security import create_token, get_current_user, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=UserRead, status_code=201)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    taken = db.query(User).filter(or_(User.username == data.username, User.email == data.email)).first()
    if taken:
        raise HTTPException(status_code=400, detail="Username or email already used")
    user = User(username=data.username, email=data.email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)  # reload so user.id is filled in
    return user


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # the "username" box can hold a username OR an email
    user = db.query(User).filter(or_(User.username == form.username, User.email == form.username)).first()
    if not user or not user.hashed_password or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong username/email or password")
    return {"access_token": create_token(user.username), "token_type": "bearer"}


@router.post("/google", response_model=Token)
def login_with_google(data: GoogleLogin, db: Session = Depends(get_db)):
    try:
        # ask Google's library: is this token real, and was it made for OUR Client ID?
        info = id_token.verify_oauth2_token(data.credential, google_requests.Request(), GOOGLE_CLIENT_ID)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    user = db.query(User).filter(User.email == info["email"]).first()
    if user is None:  # first time with Google: create the user (no password)
        user = User(username=info["email"], email=info["email"])
        db.add(user)
        db.commit()
        db.refresh(user)
    return {"access_token": create_token(user.username), "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)):
    return user