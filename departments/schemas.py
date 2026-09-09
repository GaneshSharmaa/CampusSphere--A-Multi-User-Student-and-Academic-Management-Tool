from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime, date

class CreateDepartment(BaseModel):
    dept_code: str = Field(max_length = 10)
    dept_name: str = Field(max_length = 50)

class ResponseDepartment(BaseModel):
    dept_code: str
    dept_name: str
    created_at: datetime
    updated_at: datetime

class UpdateDepartment(BaseModel):
    dept_code: str | None = None
    dept_name: str | None = None

class DeptQueryParam(UpdateDepartment):
    dept_code: str | None = None
    dept_name: str | None = None

