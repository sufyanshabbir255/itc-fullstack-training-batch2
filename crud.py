
from database import load_students, save_students
# CREATE
def create_student(student_id, student):
    students = load_students()
    if str(student_id) in students:
        return None
    students[str(student_id)] = student.model_dump()
    save_students(students)
    return students[str(student_id)]

# READ ALL
def get_all_students():
    return load_students()


# READ BY ID
def get_student(student_id):
    students = load_students()
    return students.get(str(student_id))


# UPDATE
def update_student(student_id, student):
    students = load_students()
    if str(student_id) not in students:
        return None
    students[str(student_id)] = student.model_dump()
    save_students(students)
    return students[str(student_id)]


# DELETE
def delete_student(student_id):
    students = load_students()
    if str(student_id) not in students:
        return False
    del students[str(student_id)]
    save_students(students)
    return True
