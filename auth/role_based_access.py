from auth.dependencies import get_current_user, get_current_user_institute_membership
from database.dependencies import get_db
from institutes.services import chk_institute_exists
from users.service import get_user_by_id
from users.models import User
from typing import Annotated
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# FUNCTION FOR ONLY ADMIN ACCESS
async def admin_access(
    institute_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    membership_chk = await get_current_user_institute_membership(
        db = db,
        current_user = current_user,
        institute_id = institute_id
    )

    if membership_chk is None or membership_chk.faculty.role.role_name != "Admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized."
        )

    return membership_chk


# FUNCTION FOR ONLY TEACHER ACCESS
async def teacher_access(
    institute_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    membership_chk = await get_current_user_institute_membership(
        db = db,
        current_user = current_user,
        institute_id = institute_id
    )

    if membership_chk is None or membership_chk.faculty.role.role_name != "Teacher":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized."
        )

    return membership_chk

