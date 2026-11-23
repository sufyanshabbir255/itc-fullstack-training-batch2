from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.database import (
    Base,
    engine,
    SessionLocal,
)

from app.models import User
from app.schemas import UserCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "FastAPI + PostgreSQL Running"
    }


@app.post("/users")
def create_user(user: UserCreate):

    db: Session = SessionLocal()

    new_user = User(
        username=user.username,
        email=user.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user