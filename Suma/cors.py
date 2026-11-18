from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get("/")
def home():
    return{"message": "How are you"}
@app.get("/Welcome")
def Welcome():
    return{"message": "Welcome to CORS"}

class Student(BaseModel):
    name:str
    rollno:int
@app.post("/student")
def create_student(student:Student):
    return{
        "message":"Student created",
        "name":student.name,
        "rollno":34

    }
@app.put("/student")
def create_student(student:Student):
    return{
        "message":"Add new Student",
        "name":student.name,
        "rollno":36
    }
@app.delete("/student")
def create_student(student:Student):
    return{
        "message":"New Student",
        "name":student.name,
        "rollno":36
    }
@app.delete("/student")
def create_student(student:Student):
    return{
        "message":"Student created",
        "name":student.name,
        "rollno":34
    }

