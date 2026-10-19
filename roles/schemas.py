# importing required module
from pydantic import BaseModel, ConfigDict

# schema for creating roles
class RoleCreate(BaseModel):
    role_name: str

# schema for role response
class RoleResponse(BaseModel):
    id: int
    role_name: str
    institute_id: int

    model_config = ConfigDict(from_attributes = True)

