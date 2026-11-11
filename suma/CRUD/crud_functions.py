students=[]

def create(name):
    students.append(name)
def read():
    print(students)

def update():
    students[0]="hi"

def delete():
    students.remove("hi")

create("hello")
read()

update()
read()

delete()
read()