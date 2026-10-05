# Import the required modules
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

# Importing the database models
from users.models import User
from students.models import Student

# Importing the schemas
from students.schemas import StudentCreate, StudentQueryParams, StudentResponse, StudentUpdate


async def create_student(
    db: AsyncSession,
    student_data: StudentCreate
) -> Student:
    user_exists = await db.scalar(
        select(User).where(User.id == student_data.user_id)
    )

    if user_exists is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )

    student_exists = await db.scalar(
        select(Student).where(
            Student.user_id == student_data.user_id
        )
    )

    if student_exists is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Student already exists."
        )

    student = Student(
        **student_data.model_dump()
    )

    db.add(student)

    await db.commit()
    await db.refresh(student)

    return student

