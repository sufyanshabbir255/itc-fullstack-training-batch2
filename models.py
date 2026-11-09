from pydantic import BaseModel, Field
class Student(BaseModel):
    name: str = Field(min_length=2)
    age: int = Field(gt=1, le=120)
    course: str
