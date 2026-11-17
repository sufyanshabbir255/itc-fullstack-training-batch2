from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
app = FastAPI()
@app.get("/")
def home():
    return{"message":"JWT Authentication API"}

#User model
class User(BaseModel):
    username:str
    password:str

#password hashing configuration
pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

#hash password
def hash_password(password):
    return pwd_context.hash(password)
#creating temporary db
users={}

#users registration
@app.post("/register")
def register(user: User):
    if user.username in users:
        raise HTTPException(
            status_code=400,
            detail="username already taken"

        )
    hashed_password=hash_password(user.password)
    users[user.username]={
        "username":user.username,
        "password":hashed_password
    }
    return{
        "message":"user registered success"
    }