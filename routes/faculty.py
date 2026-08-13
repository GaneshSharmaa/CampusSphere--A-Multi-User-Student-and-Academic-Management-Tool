# Importing required modules
from fastapi import HTTPException, status, Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Annotated

# Importing the database dependencies
from database.dependencies import get_db

# Importing the database models
from models.users import User
from models.faculty import Faculty
from models.roles import Role

# Importing the schemas
from schemas.faculty import FacultyCreate, FacultyResponse, FacultyUpdate, FacultyQueryParams

# Importing authentication and authorization modules
from auth.dependencies import get_current_user, admin_access, professor_access, hod_access, principal_access

router = APIRouter()

# ------ GET FACULTY INFORMATION ROUTE BY QUERY PARAMETER ------
@router.get("/search", response_model = list[FacultyResponse])
async def get_faculty_info(
    param: Annotated[FacultyQueryParams, Query()],
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Query
    query = select(Faculty)

    # Query parameter for each field
    if param.user_id is not None:
        query = query.where(Faculty.user_id.ilike(param.user_id))
    if param.first_name is not None:
        query = query.where(Faculty.first_name.ilike(f"%{param.first_name}%"))
    if param.last_name is not None:
        query = query.where(Faculty.last_name.ilike(f"%{param.last_name}%"))
    if param.dob is not None:
        query = query.where(Faculty.dob == param.dob)
    if param.sex is not None:
        query = query.where(Faculty.sex == param.sex)
    if param.address is not None:
        query = query.where(Faculty.address.ilike(f"%{param.address}%"))
    if param.date_of_joining is not None:
        query = query.where(Faculty.date_of_joining == param.date_of_joining)
    if param.dept_code is not None:
        query = query.where(Faculty.dept_code.ilike(f"%{param.dept_code}%"))
    if param.role is not None:
        query = query.join(
            Faculty.role
        ).options(
            selectinload(Faculty.role)
        ).where(
            Role.role_name == param.role
        )

    results = await db.scalars(query)
    faculties = results.all()

    return faculties

# --------- CREATING FACULTY ROUTE ---------
@router.post("/create", response_model = FacultyResponse)
async def create_faculty(
    faculty: FacultyCreate,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if user exists
    user_exists = await db.scalar(
        select(User).where(User.id == faculty.user_id)
    )

    # If not, raise HTTP exception
    if user_exists is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )

    # Check if the faculty exists
    faculty_exists = await db.scalar(
        select(Faculty).where(Faculty.user_id == faculty.user_id)
    )

    # If yes, raise HTTP exception
    if faculty_exists is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Faculty already exists."
        )

    # Object
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

# ------- UPDATE FACULTY INFORMATION ROUTE -------
@router.patch("/update/{emp_id}", response_model = FacultyResponse)
async def partial_update_faculty(
    emp_id: int,
    faculty: FacultyUpdate,
    access: Annotated[AsyncSession, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if the faculty exists
    updated_faculty = await db.scalar(
        select(Faculty).where(Faculty.emp_id == emp_id)
    )

    # If not, raise HTTP exception
    if updated_faculty is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Faculty doesn't exists."
        )

    # Setting the values into the new object
    for key, value in faculty.model_dump(exclude_unset = True).items:
        setattr(updated_faculty, key, value)

    db.add(updated_faculty)
    await db.commit()
    await db.refresh(updated_faculty)

    return updated_faculty

# --------- DELETE A FACULTY ROUTE ---------
@router.delete("/delete/{emp_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_faculty(
    emp_id: int,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if faculty exists
    faculty = await db.scalar(
        select(Faculty).where(Faculty.emp_id == emp_id)
    )

    # If not, raise HTTP exception
    if faculty is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Faculty doesn't exists."
        )

    await db.delete(faculty)
    await db.commit()

