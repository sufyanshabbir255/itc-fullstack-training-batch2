"""
app/schemas/item.py
-------------------
Pydantic models (schemas) for the "Item" resource.

THE PATTERN: one model per *purpose*
    ItemBase    -> fields shared by every other model
    ItemCreate  -> body for POST   (what the client sends to create)
    ItemUpdate  -> body for PUT    (full replacement; same fields as create)
    ItemPatch   -> body for PATCH  (partial update; every field optional)
    ItemOut     -> used as `response_model` (what the API returns)

WHY NOT ONE MODEL FOR EVERYTHING?
    - The client must NOT send `id` or `created_at` – the server sets them.
    - The response MUST include `id` and `created_at`.
    - A partial update needs every field to be optional.
    Separate models make each contract explicit and keep the OpenAPI docs
    accurate.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    # Field(...) adds validation rules AND documentation.
    #   `...`  (Ellipsis)   -> the field is required
    #   min_length/gt/...   -> validation; violating them returns HTTP 422
    #   description/examples-> shown in Swagger UI
    name: str = Field(..., min_length=1, max_length=100, examples=["Laptop"])
    description: Optional[str] = Field(
        default=None, max_length=500, examples=["14-inch, 16GB RAM"]
    )
    price: float = Field(..., gt=0, description="Price must be greater than 0", examples=[999.99])
    in_stock: bool = Field(default=True, examples=[True])


class ItemCreate(ItemBase):
    """Request body for POST /items. Inherits all fields from ItemBase."""

    # `model_config` with json_schema_extra sets the example shown
    # in the "Request body" box of Swagger UI.
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Mechanical Keyboard",
                "description": "RGB, brown switches",
                "price": 79.5,
                "in_stock": True,
            }
        }
    )


class ItemUpdate(ItemBase):
    """
    Request body for PUT /items/{item_id}.
    PUT = *replace the whole resource*, so all required fields are required
    again (identical to ItemCreate, but a separate class keeps docs clear).
    """


class ItemPatch(BaseModel):
    """
    Request body for PATCH /items/{item_id}.
    PATCH = *partial update*, so every field is Optional. Only the fields the
    client actually sends will be changed (see `exclude_unset` in the router).
    """

    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[float] = Field(default=None, gt=0)
    in_stock: Optional[bool] = None


class ItemOut(ItemBase):
    """
    The RESPONSE model.

    When a route declares `response_model=ItemOut`, FastAPI will:
      1. Validate the returned data against this model.
      2. FILTER OUT any field not declared here (e.g. secret/internal fields).
      3. Document the response shape in OpenAPI.
    """

    id: int = Field(..., examples=[1])
    created_at: datetime

    # from_attributes=True lets Pydantic read data from objects
    # (e.g. ORM models like SQLAlchemy) and not only from dicts.
    model_config = ConfigDict(from_attributes=True)
