# Importing required modules
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

# Importing the database dependencies
from database.dependencies import get_db

# Importing the database models
from membership.models import Membership
# Importing the schemas
from departments.schemas import CreateDepartment, ResponseDepartment, UpdateDepartment, DeptQueryParam
from departments.service import search_departments, create_new_department, update_department, delete_department
from departments.exceptions import DepartmentNotFoundError, DuplicateDepartmentError

# Importing authentication and authorization modules
from auth.role_based_access import require_admin

router = APIRouter()


# Route for getting the department
@router.get("/departments", response_model = list[ResponseDepartment])
async def search_dept(
    db: Annotated[AsyncSession, Depends(get_db)],
    membership: Annotated[Membership, Depends(require_admin)],
    department_data: Annotated[DeptQueryParam, Depends()]
):
    return await search_departments(
        db = db,
        institute_id = membership.institute_id,
        params = department_data
    )


# Route for creating a department
@router.post("/create-department", response_model = ResponseDepartment)
async def create_department(
    db: Annotated[AsyncSession, Depends(get_db)],
    membership: Annotated[Membership, Depends(require_admin)],
    department_data: CreateDepartment
):
    try:
        return await create_new_department(
            db = db,
            institute_id = membership.institute_id,
            department_data = department_data
        )
    except DuplicateDepartmentError as error:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = str(error),
        ) from error


# Route for updating a department
@router.patch("/update-department/{department_id}", response_model = ResponseDepartment)
async def update_department_route(
    department_id: int,
    department_data: UpdateDepartment,
    db: Annotated[AsyncSession, Depends(get_db)],
    membership: Annotated[Membership, Depends(require_admin)],
):
    try:
        return await update_department(
            db = db,
            institute_id = membership.institute_id,
            department_id = department_id,
            department_data = department_data,
        )
    except DepartmentNotFoundError as error:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(error),
        ) from error
    except DuplicateDepartmentError as error:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = str(error),
        ) from error


# Route for deleting a department
@router.delete("/delete-department/{department_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_department_route(
    department_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    membership: Annotated[Membership, Depends(require_admin)],
):
    try:
        await delete_department(
            db = db,
            institute_id = membership.institute_id,
            department_id = department_id,
        )
    except DepartmentNotFoundError as error:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(error),
        ) from error

