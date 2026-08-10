from pydantic import BaseModel, Field
from typing import Annotated

class CreateDepartment(BaseModel):
    dept_code: str = Field(max_length = 10)
    dept_name: str = Field(max_length = 50)

class ResponseDepartment(BaseModel):
    dept_code: str
    dept_name: str

class UpdateDepartment(BaseModel):
    dept_code: str | None = None
    dept_name: str | None = None

