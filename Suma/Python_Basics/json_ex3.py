import json
employee = {
 "employee_name" : "sam",
 "employee_id" : 501,
 "age" : 28,
 "department" : "IT",
 "skills" : ["python","java"],
 "experience":2
}
json_data = json.dumps(employee, indent=4)
print(json_data)
print(employee["employee_id"]),
print(employee["employee_name"]),
print(employee["age"])
print(employee["skills"])
