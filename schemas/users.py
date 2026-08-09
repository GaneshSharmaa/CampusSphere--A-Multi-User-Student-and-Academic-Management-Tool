from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr

# schema for request validation - user creating / registering
class UserCreate(BaseModel):
    email: EmailStr
    phone: str
    password: str

# schema for response model - user response
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    phone: str

    model_config = ConfigDict(from_attributes = True)

# schema for request validation - user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for query parameter
class UserQueryParams(BaseModel):
    email: str | None = None
    phone: str | None = None

