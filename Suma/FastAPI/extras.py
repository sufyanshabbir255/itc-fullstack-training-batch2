from fastapi import FastAPI, Response,Request
app=FastAPI()
#save cookie
@app.post("/save")
def save_cookie(response:Response):
    response.set_cookie("name","suma")
    return{"message":"cookie saved"}

#get cookie
@app.get("/get")
def get_cookie(request:Request):
    name=request.cookies.get("name")
    return{"name":name}

from fastapi import Header

#get api-which read header
@app.get("/pizza")
def order_pizza(
    customer_name:str= Header(),
    pizza_type:str=Header()
):
    return{
        "customer":customer_name,
        "pizza" :pizza_type,
        "message":"order received"

    }


from pydantic import BaseModel
#giving customer details
class customer(BaseModel):
    name:str
    contact:str
    
#giving delivery address
class delivery(BaseModel):
    address:str
    place:str
    postcode:str

class pizzaorder(BaseModel):
     customer:customer
     pizza:str
     quantity:int
     delivery:delivery

#post api
@app.post("/pizza-order")
def create_order(order: pizzaorder):
    return{
        "message":"order successfull","order_details":order
    }