from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional


class TaskBase(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["What needs to be done?"]
    )

    priority: Literal[
        "Low",
        "Medium",
        "High"
    ] = Field(
        default="Medium"
    )

    isComplete: bool = Field(
        default=False
    )


class TaskCreate(TaskBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Clean the dishes",
                "priority": "High"
            }
        }
    )


class TaskUpdate(TaskBase):
    pass


class TaskPatch(BaseModel):
    text: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    priority: Optional[
        Literal[
            "Low",
            "Medium",
            "High"
        ]
    ] = None

    isComplete: Optional[bool] = None


class TaskOut(TaskBase):
    id: int = Field(
        ...,
        examples=[1]
    )

    model_config = ConfigDict(
        from_attributes=True
    )