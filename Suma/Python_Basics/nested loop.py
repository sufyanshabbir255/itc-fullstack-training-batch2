#loop inside another loop
for i in range(3):#1st loop
    for j in range(4):#2nd loop
        print(i,j)
students=["hi","hello"]
courses=["python","sql"]

for student in students:
    for course in courses:
        print(students,courses)

for student in students:
    print("student:",students)
    for course in courses:

        print(courses)