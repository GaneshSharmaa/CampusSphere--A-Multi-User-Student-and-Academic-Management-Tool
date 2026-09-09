# Importing required modules
from fastapi import HTTPException, status, Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Annotated

# Importing the database dependencies
from database.dependencies import get_db

# Importing the database models
from roles.models import User
from students.models import Student

# Importing the schemas
from students.schemas import StudentCreate, StudentResponse, StudentQueryParams, StudentUpdate

# Importing authentication and authorization modules
from auth.dependencies import get_current_user, admin_access, professor_access, hod_access, principal_access

router = APIRouter()

# ----------- GET STUDENT INFO ROUTE -----------
@router.get("/search", response_model = list[StudentResponse])
async def get_student_info(
    param: Annotated[StudentQueryParams, Query()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if current logged in user is in student table
    student_chk = await db.scalar(
        select(Student).where(Student.user_id == current_user.id)
    )

    # If yes, raise HTTP exception
    if student_chk is not None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized."
        )

    # Query
    query = select(Student)

    # Query parameters
    if param.first_name is not None:
        query = query.where(
            Student.first_name.ilike(f"%{param.first_name}%")
        )
    if param.last_name is not None:
        query = query.where(
            Student.last_name.ilike(f"%{param.last_name}%")
        )
    if param.dob is not None:
        query = query.where(
            Student.dob == param.dob
        )
    if param.sex is not None:
        query = query.where(
            Student.sex == param.sex
        )
    if param.address is not None:
        query = query.where(
            Student.address.ilike(f"%{param.address}%")
        )
    if param.date_of_admission is not None:
        query = query.where(
            Student.date_of_admission == param.date_of_admission
        )
    if param.dept_code is not None:
        query = query.where(
            Student.dept_code.ilike(f"%{param.dept_code}%")
        )
    if param.start_batch_year is not None:
        query = query.where(
            Student.start_batch_year == param.start_batch_year
        )
    if param.end_batch_year is not None:
        query = query.where(
            Student.end_batch_year == param.end_batch_year
        )

    result = await db.scalars(query)
    students = result.all()
    return students

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

# ------- PATCH ROUTE - UPDATE STUDENT INFORMATION -------
@router.patch("/update/{student_id}", response_model = StudentResponse)
async def update_student(
    student_id: int,
    student_detail: StudentUpdate,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if student with student_id exists
    student = await db.scalar(
        select(Student).where(Student.id == student_id)
    )

    # If no, raise HTTP exception
    if student is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Student doesn't exists."
        )

    for key, value in student_detail.model_dump(exclude_unset = True).items():
        setattr(student, key, value)

    db.add(student)
    await db.commit()
    await db.refresh(student)

    return student

# DELETE ROUTE - DELETE STUDENT INFORMATION
@router.delete("/delete/{student_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if student with student_id exists
    student = await db.scalar(
        select(Student).where(Student.id == student_id)
    )

    # If no, raise HTTP exception
    if student is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Student not found."
        )

    await db.delete(student)
    await db.commit()

