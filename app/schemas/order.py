# added by Din: schemas for the NESTED BODY demo (models inside models)
from pydantic import BaseModel, Field


class Address(BaseModel):
    street: str = Field(..., examples=["10 Downing Street"])
    city: str = Field(..., examples=["London"])
    postcode: str = Field(..., examples=["SW1A 2AA"])


class OrderLine(BaseModel):
    product: str = Field(..., examples=["Laptop"])
    quantity: int = Field(..., gt=0, examples=[2])
    unit_price: float = Field(..., gt=0, examples=[999.99])


class Order(BaseModel):
    customer_name: str = Field(..., examples=["Hasnaad Din"])
    delivery_address: Address                       # a model INSIDE a model
    lines: list[OrderLine] = Field(..., min_length=1)  # a LIST of models (at least 1)
    tags: list[str] = []                            # a simple list of text, optional