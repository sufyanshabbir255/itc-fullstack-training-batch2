from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.permissions import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)  # bcrypt uses max 72 bytes
    full_name: str | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = Field(default=None, min_length=8, max_length=72)


class RoleUpdate(BaseModel):
    role: Role


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str | None
    role: Role
    is_active: bool
    created_at: datetime
