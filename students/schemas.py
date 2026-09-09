# Importing the required modules
from pydantic import BaseModel, Field, PastDate, ConfigDict
from datetime import date, datetime

# Importing the Sex Enum
from faculties.models import SexEnum

# Schema for creating a student
class StudentCreate(BaseModel):
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
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes = True)

# Schema for Student query parameter
class StudentQueryParams(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    dob: date | None = None
    sex: SexEnum | None = None
    address: str | None = None
    date_of_admission: date | None = None
    dept_code: str | None = None
    start_batch_year: int | None = None
    end_batch_year: int | None = None

# Schema for updating student
class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    dob: date | None = None
    sex: SexEnum | None = None
    address: str | None = None
    date_of_admission: date | None = None
    start_batch_year: int | None = None
    end_batch_year: int | None = None
    dept_code: str | None = None

