import json
student = {
"name" : "isha",
"age": 22,
"subjects" : ["eng","math","sci"],
"place" : "london",
}
json_data=json.dumps(student,indent=4)
print(json_data)