# schemas.py - Pydantic schemas = the shape of data going IN and OUT of the API
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):      # IN: signup form
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):        # OUT: never includes the password
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}  # lets Pydantic read a SQLAlchemy object


class Token(BaseModel):           # OUT: after login
    access_token: str
    token_type: str


class GoogleLogin(BaseModel):     # IN: the token Google gave the browser
    credential: str


class PostCreate(BaseModel):      # IN: new post form
    title: str
    content: str


class PostRead(BaseModel):        # OUT: a saved post
    id: int
    title: str
    content: str
    created_at: datetime
    user_id: int

    model_config = {"from_attributes": True}