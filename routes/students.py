# Importing required modules
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Annotated

# Importing the database dependencies
from database.dependencies import get_db

# Importing the database models
from models.users import User
from models.students import Student

# Importing the schemas
from schemas.students import StudentCreate, StudentResponse

# Importing authentication and authorization modules
from auth.dependencies import get_current_user, admin_access, professor_access, hod_access, principal_access

router = APIRouter()

# ------- POST ROUTE - FOR CREATING A STUDENT -------
@router.post("/create", response_model = StudentResponse)
async def create_student(
    student: StudentCreate,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if user with user_id exists or not
    user_exists = await db.scalar(
        select(User).where(
            User.id == student.user_id
        )
    )

    # If the user not exists, then raise HTTP exception
    if user_exists is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )

    # Check if student already exists
    student_exists = await db.scalar(
        select(Student).where(
            Student.user_id == student.user_id
        )
    )

    # If exists, then raise HTTP exception
    if student_exists is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Student already exists."
        )

    student_detail = Student(
        **student.model_dump()
    )

    db.add(student_detail)
    await db.commit()
    await db.refresh(student_detail)

    return student_detail

