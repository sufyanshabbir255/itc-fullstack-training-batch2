"""
app/schemas/user.py
-------------------
Schemas for the "User" resource.

THE KEY LESSON HERE: response_model protects sensitive data.
    UserCreate contains a `password`.
    The stored user contains a `hashed_password`.
    UserOut contains NEITHER.

    Even though the router returns the full stored dict (including
    `hashed_password`), declaring `response_model=UserOut` makes FastAPI strip
    every field not listed in UserOut. The password never leaks.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, examples=["romesh"])
    # EmailStr validates the format (needs the `email-validator` package,
    # which is included in fastapi[standard]).
    email: EmailStr = Field(..., examples=["romesh@example.com"])
    full_name: str | None = Field(default=None, examples=["Romesh Bansal"])


class UserCreate(UserBase):
    """Request body for POST /users. Includes a plain-text password."""
    password: str = Field(..., min_length=8, examples=["supersecret123"])
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username"  : "A_dog_that_sits"
                ,"email"    : "john_doe@example.com"
                ,"full_name": "Johnathan Doe"
                ,"password" : "password"
            }
        }
    )

class UserOut(UserBase):
    """Response model: NO password fields at all."""
    id: int
    is_active: bool = True
    model_config = ConfigDict(from_attributes=True)

class UserPatch(BaseModel):
    username: Optional[str] = Field(defailt=None, min_length=3, max_length=30)
    email: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None, min_length=8)
    full_name: Optional[str] = None