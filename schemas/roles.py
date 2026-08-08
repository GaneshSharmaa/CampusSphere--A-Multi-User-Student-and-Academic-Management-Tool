# importing required module
from pydantic import BaseModel

# schema for creating roles
class RoleCreate(BaseModel):
    role_name: str

# schema for role response
class RoleResponse(BaseModel):
    role_name: str

