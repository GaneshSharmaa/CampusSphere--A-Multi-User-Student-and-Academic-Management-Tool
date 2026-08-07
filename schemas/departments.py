from pydantic import BaseModel, Field
from typing import Annotated

class CreateDepartment(BaseModel):
    dept_code: str = Field(max_length = 10)
    dept_name: str = Field(max_length = 50)

