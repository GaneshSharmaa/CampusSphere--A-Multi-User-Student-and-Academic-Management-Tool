# Importing the required modules
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# Schema for creating an institution
class InstituteCreate(BaseModel):
    institute_name: str

# Schema for having institution response
class InstituteResponse(BaseModel):
    id: int
    institute_code: str
    institute_name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes = True)

