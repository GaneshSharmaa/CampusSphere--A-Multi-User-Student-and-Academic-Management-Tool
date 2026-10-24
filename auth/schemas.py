from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str

class InstituteSummary(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes = True)

