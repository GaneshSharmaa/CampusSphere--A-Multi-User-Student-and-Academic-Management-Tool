# Importing the required modules
from fastapi import HTTPException, status, Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

# Importing the authentication dependency
from auth.dependencies import get_current_user

# Importing the database dependencies
from database.dependencies import get_db

# Importing the custom exceptions
from institutes.exceptions import DuplicateInstituteError

# Importing the schemas
from institutes.schemas import InstituteCreate, InstituteResponse

# Importing the business logic from the service layer
from institutes.services import create_institute

# Importing the User model
from users.models import User

router = APIRouter()

# --------- CREATE INSTITUTE ROUTE ---------
@router.post("/create", response_model = InstituteResponse)
async def create_institute_route(
    institute: InstituteCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        return await create_institute(
            db=db,
            institute_data=institute,
        )
    except DuplicateInstituteError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

