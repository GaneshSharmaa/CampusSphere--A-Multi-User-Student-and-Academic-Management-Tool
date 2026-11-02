# Importing the User database model
from faculties.models import Faculty

# Importing the faculties schema
from faculties.schemas import FacultyCreate

# Importing the required modules
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from users.service import get_user_by_id


# Function to check if faculty exists or not
async def chk_faculty_exists(user_id: int, institute_id: int, db: AsyncSession) -> Faculty | None:
    """
    Fetches a faculty from the database by their unique ID.
    Returns the Faculty database model object if found, otherwise returns None.
    """
    statement = select(Faculty).where(Faculty.id == user_id)

    faculty = await db.scalar(statement)

    return faculty

# Function to add a faculty
async def add_faculty(db: AsyncSession, faculty: FacultyCreate, institute_id: int):
    """
    Validate the business requirements and creates a new faculty records.
    """
    user_exists = get_user_by_id(user_id = faculty.user_id, db = db)

    if user_exists is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )

    faculty_exists = chk_faculty_exists(user_id = faculty.user_id, institute_id = institute_id, db = db)

    if faculty_exists is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Faculty already exists."
        )

    new_faculty = Faculty(
        user_id = faculty.user_id,
        first_name = faculty.first_name,
        last_name = faculty.last_name,
        dob = faculty.dob,
        sex = faculty.sex,
        address = faculty.address,
        date_of_joining = faculty.date_of_joining,
        dept_id = faculty.dept_id,
        role_id = faculty.role_id,
        institute_id = institute_id,
    )

    db.add(new_faculty)
    await db.commit()
    await db.refresh(new_faculty)

    return new_faculty

