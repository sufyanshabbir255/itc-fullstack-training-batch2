import json #1st import json 
student = { #---> {} these are for start & end object

    "name" : "suma", #(: seperates key value)
    "roll_num" : 23, #(, seperate to diff items)
    "course" : ["python","sql","java"]
}
json_data = json.dumps(student,indent=4)
print(json_data)

