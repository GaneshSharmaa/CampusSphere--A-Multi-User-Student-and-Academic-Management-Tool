from pydantic import BaseModel, PastDate, ConfigDict
from datetime import date, datetime
from models.faculty import SexEnum

class FacultyCreate(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    dob: PastDate
    sex: SexEnum
    address: str
    date_of_joining: date
    dept_code: str
    role_id: int

class FacultyResponse(BaseModel):
    emp_id: int
    user_id: int
    first_name: str
    last_name: str
    dob: PastDate
    sex: SexEnum
    address: str
    date_of_joining: date
    dept_code: str
    role_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes = True)

