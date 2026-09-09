# Importing the required modules
from pydantic import BaseModel, PastDate, ConfigDict
from datetime import date, datetime

# Importing the Sex Enum for sex
from faculties.models import SexEnum

# Schema for creating faculty
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

# Schema for reponse faculty
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

# Schema for Faculty update
class FacultyUpdate(BaseModel):
    user_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    dob: PastDate | None = None
    sex: SexEnum | None = None
    address: str | None = None
    date_of_joining: date | None = None
    dept_code: str | None = None
    role: str | None = None

# Schema for Faculty query parameter
class FacultyQueryParams(FacultyUpdate):
    pass

