from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, PastDate

# schema for request validation - user creating / registering
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    dob: PastDate
    phone: str
    email: EmailStr
    password: str

# schema for updating user
class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    dob: PastDate | None = None

# schema for response model - user response
class UserResponse(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr

    model_config = ConfigDict(from_attributes = True)

# schema for request validation - user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# schema for query parameters
class UserQueryParams(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    dob: PastDate | None = None

