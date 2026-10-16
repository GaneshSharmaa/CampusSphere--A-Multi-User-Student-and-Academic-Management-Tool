# Importing required modules
from fastapi import status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

# Importing the database dependencies
from database.dependencies import get_db

# Importing the database models
from users.models import User

# Importing the schemas
from students.schemas import StudentCreate, StudentResponse, StudentQueryParams, StudentUpdate

# Importing authentication and authorization modules
from auth.dependencies import get_current_user, admin_access, professor_access, hod_access, principal_access

# Importing the services
from students.service import (
    create_new_student,
    delete_student as delete_student_service,
    search_student,
    update_student as update_student_service,
)

router = APIRouter()

# ----------- GET STUDENT INFO ROUTE -----------
@router.get("/search", response_model = list[StudentResponse])
async def get_student_info(
    param: Annotated[StudentQueryParams, Depends()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await search_student(db, param, current_user)

# ------- POST ROUTE - FOR CREATING A STUDENT -------
@router.post("/create", response_model = StudentResponse)
async def create_student(
    student: StudentCreate,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await create_new_student(
        db = db,
        student_data = student,
        current_user = access,
    )

# ---------- PATCH ROUTE - UPDATE STUDENT INFORMATION ----------
@router.patch("/update/{student_id}", response_model = StudentResponse)
async def update_student_route(
    student_id: int,
    student_data: StudentUpdate,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await update_student_service(
        db = db,
        student_id = student_id,
        student_data = student_data,
        current_user = access,
    )

# -------- DELETE ROUTE - DELETE STUDENT INFORMATION --------
@router.delete("/delete/{student_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_student_route(
    student_id: int,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await delete_student_service(
        db = db,
        student_id = student_id,
        current_user = access,
    )

