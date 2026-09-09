
from fastapi import HTTPException, status, Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Annotated

# Importing the database dependencies
from database.dependencies import get_db

# Importing the database models
from institutes.models import Institute

# Importing the business logic from the service layer
from institutes.services import generate_code

# Importing the schemas
from institutes.schemas import InstituteCreate, InstituteResponse

router = APIRouter()

# --------- CREATE INSTITUTE ROUTE ---------
@router.post("/create", response_model = InstituteResponse)
async def create_institute(
    db: Annotated[AsyncSession, Depends(get_db)],
    institute: InstituteCreate
):
    code = generate_code()
    
    new_institute = Institute(
        institute_code = code,
        institute_name = institute.institute_name
    )

    db.add(new_institute)
    await db.commit()
    await db.refresh(new_institute)

    return new_institute

