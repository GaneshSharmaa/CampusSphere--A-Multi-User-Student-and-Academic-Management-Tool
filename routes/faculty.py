# Importing required modules
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Annotated

# Importing the database dependencies
from database.dependencies import get_db

# Importing the database models
from models.users import User
from models.faculty import Faculty

# Importing the schemas
from schemas.faculty import FacultyCreate, FacultyResponse

# Importing authentication and authorization modules
from auth.dependencies import get_current_user, admin_access, professor_access, hod_access, principal_access

router = APIRouter()

# --------- CREATING FACULTY ROUTE ---------
@router.post("/create", response_model = FacultyResponse)
async def create_faculty(
    faculty: FacultyCreate,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    faculty_exists = await db.scalar(
        select(Faculty).where(Faculty.user_id == faculty.user_id)
    )

    if faculty_exists is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Faculty already exists."
        )

    user_exists = await db.scalar(
        select(User).where(User.id == faculty.user_id)
    )

    if user_exists is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )

    faculty_detail = Faculty(
        user_id = faculty.user_id,
        first_name = faculty.first_name,
        last_name = faculty.last_name,
        dob = faculty.dob,
        sex = faculty.sex,
        address = faculty.address,
        date_of_joining = faculty.date_of_joining,
        dept_code = faculty.dept_code,
        role_id = faculty.role_id,
    )

    db.add(faculty_detail)
    await db.commit()
    await db.refresh(faculty_detail)

    return faculty_detail

