from datetime import datetime

from pydantic import BaseModel, ConfigDict

from institutes.schemas import InstituteResponse


class MembershipCreate(BaseModel):
    institute_id: int


class MembershipResponse(BaseModel):
    id: int
    user_id: int
    institute_id: int
    created_at: datetime
    institute: InstituteResponse

    model_config = ConfigDict(from_attributes = True)

