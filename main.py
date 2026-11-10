
from fastapi import FastAPI, HTTPException, status
from models import Student
from crud import (
    create_student,
    get_all_students,
    get_student,
    update_student,
    delete_student
)

app = FastAPI(title="Student Management CRUD API")

# HOME API
@app.get("/")
def home():
    return {"message": "Welcome to Student Management API"}

# CREATE STUDENT
@app.post("/students/{student_id}", status_code=status.HTTP_201_CREATED)
def add_student(student_id: int, student: Student):
    result = create_student(student_id, student)
    if result is None:
        raise HTTPException(
            status_code=409,
            detail="Student already exists"
        )
    return {
        "message": "Student created successfully",
        "data": result
    }

# READ ALL STUDENTS
@app.get("/students")
def read_students():
    return get_all_students()

# READ STUDENT BY ID
@app.get("/students/{student_id}")
def read_student(student_id: int):
    result = get_student(student_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return result

# UPDATE STUDENT
@app.put("/students/{student_id}")
def edit_student(student_id: int, student: Student):
    result = update_student(student_id, student)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student updated successfully",
        "data": result
    }


# DELETE STUDENT
@app.delete("/students/{student_id}")
def remove_student(student_id: int):
    result = delete_student(student_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return {
        "message": "Student deleted successfully"
    }
