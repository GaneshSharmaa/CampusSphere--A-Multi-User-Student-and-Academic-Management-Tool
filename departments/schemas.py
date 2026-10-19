from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CreateDepartment(BaseModel):
    dept_code: str = Field(max_length = 10)
    dept_name: str = Field(max_length = 50)

class ResponseDepartment(BaseModel):
    id: int
    dept_code: str
    dept_name: str
    institute_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes = True)

class UpdateDepartment(BaseModel):
    dept_code: str | None = None
    dept_name: str | None = None

class DeptQueryParam(UpdateDepartment):
    dept_code: str | None = None
    dept_name: str | None = None

