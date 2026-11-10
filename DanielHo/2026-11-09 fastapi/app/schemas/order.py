from pydantic import BaseModel

class Address(BaseModel):
    street  : str
    city    : str
    address : Address

class Customer(BaseModel):
    name    : str
    email   : str
    address : Address

class Order(BaseModel):
    order_id: int
    customer: Customer