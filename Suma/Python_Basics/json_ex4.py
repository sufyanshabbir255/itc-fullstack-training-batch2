import json
order= {
"customer_name" : "yash",
"order_id" : 27,
"product" : "dress",
"price":650,
"quantity" : 4,
"status" : True #why the 't' should be uppercase? when it is json?
}
json_data=json.dumps("order", indent=4)
print(json_data)
print(order["customer_name"]),
print(order["status"])