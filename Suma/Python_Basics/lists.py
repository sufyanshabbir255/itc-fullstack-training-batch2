#mutable-add,insert,remove,delete
courses=["python" ,"java","databricks"]
print(courses)

courses=["python" ,"java","databricks"]
courses.append("sql")
print(courses)

courses=["python" ,"java","databricks","sql"]
courses.remove("sql")
print(courses)

names=["123","456","678"]
print(names[0])
print(names[2])

names=["123","456","678","999"]
print(names[-0])
print(names[-2])



#adding item--insert
courses=["python" ,"java","databricks"]
courses.insert(2,"sql")
print(courses)

#update
courses=["python" ,"java","databricks"]
courses[2]="sql"
print(courses)

#length
numbers=[1,2,3,4,5,6]
print(len(numbers))

#reverse
numbers=[1,2,3,4,5,6]
numbers.reverse()
print(numbers)

#max min
numbers=[30,1,45,66,78]
print("maxium:",max(numbers))
print("minimum:",min(numbers))

