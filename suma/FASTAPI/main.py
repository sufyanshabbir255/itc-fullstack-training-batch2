from fastapi import FastAPI
app = FastAPI()
students=[]

@app.post("/add")
def add_student():
    students.append("hello")
    return students
@app.get("/students")
def get_students():
    return students