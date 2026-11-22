# Importing required modules
from fastapi import HTTPException, status, Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

# Importing the database dependencies
from database.dependencies import get_db

# Importing the schemas
from faculties.schemas import FacultyCreate, FacultyResponse, FacultyUpdate, FacultyQueryParams

# Importing authentication and authorization modules
from auth.role_based_access import require_admin

# Importing the faculty services
from faculties.service import (
    add_faculty,
    delete_faculty as delete_faculty_service,
    search_faculties,
    update_faculty,
)

# Importing the exceptions
from faculties.exceptions import (
    DuplicateFacultyError,
    FacultyNotFoundError,
    FacultyReferenceNotFoundError,
)

# Importing the membership model
from membership.models import Membership

router = APIRouter()


# ------ GET FACULTY INFORMATION ROUTE BY QUERY PARAMETER ------
@router.get("/search", response_model = list[FacultyResponse])
async def get_faculty_info(
    param: Annotated[FacultyQueryParams, Query()],
    membership: Annotated[Membership, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    return await search_faculties(
        db = db,
        institute_id = membership.institute_id,
        params = param,
    )


# --------- CREATING FACULTY ROUTE ---------
@router.post("/create", response_model = FacultyResponse)
async def create_faculty(
    faculty: FacultyCreate,
    membership: Annotated[Membership, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        return await add_faculty(
            db = db,
            faculty = faculty,
            institute_id = membership.institute_id,
        )
    except DuplicateFacultyError as error:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = str(error)
        ) from error
    except FacultyReferenceNotFoundError as error:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(error)
        ) from error


# ------- UPDATE FACULTY INFORMATION ROUTE -------
@router.patch("/update/{emp_id}", response_model = FacultyResponse)
async def partial_update_faculty(
    emp_id: int,
    faculty: FacultyUpdate,
    membership: Annotated[Membership, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        return await update_faculty(
            db = db,
            institute_id = membership.institute_id,
            emp_id = emp_id,
            faculty_data = faculty,
        )
    except FacultyNotFoundError as error:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(error)
        ) from error
    except DuplicateFacultyError as error:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = str(error)
        ) from error
    except FacultyReferenceNotFoundError as error:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(error)
        ) from error


# --------- DELETE A FACULTY ROUTE ---------
@router.delete("/delete/{emp_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_faculty(
    emp_id: int,
    membership: Annotated[Membership, Depends(require_admin)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    try:
        await delete_faculty_service(
            db = db,
            institute_id = membership.institute_id,
            emp_id = emp_id,
        )
    except FacultyNotFoundError as error:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = str(error)
        ) from error

