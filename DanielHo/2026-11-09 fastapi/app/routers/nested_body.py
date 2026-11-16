# \routers\nested_body.py

from fastapi import APIRouter

from app.schemas.order import Order

router = APIRouter(
    prefix  ="/orders",
    tags    =["Nested Bodies"],
)

@router.post("/")
def create_order(order: Order):
    return order