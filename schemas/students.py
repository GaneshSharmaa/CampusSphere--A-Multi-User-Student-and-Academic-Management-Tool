# Importing the required modules
from pydantic import BaseModel, Field, PastDate, ConfigDict
from datetime import date, datetime

# Importing the Sex Enum
from models.faculty import SexEnum

# Schema for creating a student
class StudentCreate(BaseModel):
    roll_no: int
    user_id: int
    first_name: str
    last_name: str
    dob: PastDate
    sex: SexEnum
    address: str
    date_of_admission: date
    dept_code: str
    start_batch_year: int
    end_batch_year: int
    role_id: int

# Schema for response model of a student
class StudentResponse(BaseModel):
    id: int
    roll_no: int
    user_id: int
    first_name: str
    last_name: str
    dob: PastDate
    sex: SexEnum
    address: str
    date_of_admission: date
    dept_code: str
    start_batch_year: int
    end_batch_year: int
    role_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes = True)

