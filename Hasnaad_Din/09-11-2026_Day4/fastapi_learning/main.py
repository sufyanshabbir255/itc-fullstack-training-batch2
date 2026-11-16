from fastapi import FastAPI, status
from pydantic import BaseModel

# Create FastAPI application
app = FastAPI()


# --------------------------
# RESPONSE MODEL
# --------------------------

# Defines the shape of a student
class Student(BaseModel):
    name: str
    age: int


# --------------------------
# GET
# --------------------------

# Visit:
# http://127.0.0.1:8000/

@app.get("/")
def home():
    return {"message": "Hello Hasnaad"}


# --------------------------
# GET WITH RESPONSE MODEL
# --------------------------

# FastAPI will make sure
# the response contains:
# name (string)
# age (integer)

@app.get(
    "/student",
    response_model=Student,
    status_code=status.HTTP_200_OK
)
def get_student():

    return {
        "name": "Hasnaad",
        "age": 44
    }


# --------------------------
# POST
# --------------------------

# Creates a student

@app.post(
    "/student",
    status_code=status.HTTP_201_CREATED
)
def create_student(name: str):

    return {
        "message": "Student created",
        "student_name": name
    }


# --------------------------
# PUT
# --------------------------

# Updates a student

@app.put(
    "/student",
    status_code=status.HTTP_200_OK
)
def update_student(name: str):

    return {
        "message": "Student updated",
        "new_name": name
    }


# --------------------------
# DELETE
# --------------------------

# Deletes a student

@app.delete(
    "/student",
    status_code=status.HTTP_200_OK
)
def delete_student():

    return {
        "message": "Student deleted"
    }