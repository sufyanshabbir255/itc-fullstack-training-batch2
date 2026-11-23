from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.database import (
    Base
    ,engine
    ,SessionLocal
)

from app.schemas import UserCreate

from app.models import User



app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "Running"
    }


@app.post("/users")
def create_user(user: UserCreate):

    db: Session = SessionLocal()

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user