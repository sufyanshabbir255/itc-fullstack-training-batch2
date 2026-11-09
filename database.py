import json
import os
FILE_PATH = "students.json"
def load_students():
    if not os.path.exists(FILE_PATH):
        return {}

    with open(FILE_PATH, "r") as file:
        return json.load(file)
def save_students(students):

    with open(FILE_PATH, "w") as file:
        json.dump(students, file, indent=4)
