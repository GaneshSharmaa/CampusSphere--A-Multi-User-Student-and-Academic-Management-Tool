# Importing required modules
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Annotated

# Importing the database dependencies
from database.dependencies import get_db

# Importing the database models
from models.users import User
from models.departments import Department

# Importing the schemas
from schemas.departments import CreateDepartment, ResponseDepartment

# Importing authentication and authorization modules
from auth.dependencies import get_current_user, admin_access, principal_access

router = APIRouter()

# POST ROUTE - CREATE DEPARTMENT ROUTE
@router.post("/create", response_model = ResponseDepartment)
async def create_department(
    department: CreateDepartment,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if department code already exists
    dept_code_exists = await db.scalar(
        select(Department).where(Department.dept_code == department.dept_code)
    )

    # Check if deparment name already exists
    dept_name_exists = await db.scalar(
        select(Department).where(Department.dept_name == department.dept_name)
    )

    # If department code exists, raise HTTP exception
    if dept_code_exists is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"Department code {dept_code_exists} already exists."
        )

    # If department name exists, raise HTTP exception
    if dept_name_exists is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"Department name {dept_name_exists} already exists."
        )

    new_dept = Department(**department.model_dump())

    db.add(new_dept)
    await db.commit()
    await db.refresh(new_dept)

    return new_dept

