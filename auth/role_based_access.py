from typing import Annotated
from fastapi import HTTPException, status, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies import get_current_user, get_current_user_institute_membership
from database.dependencies import get_db
from users.models import User

# FUNCTION FOR ONLY ADMIN ACCESS
async def admin_access(
    institute_id: Annotated[int, Header(alias = "X-Institute-ID")],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> int:
    membership_exists = await get_current_user_institute_membership(
        db = db,
        current_user = current_user,
        institute_id = institute_id
    )

    if membership_exists is None or membership_exists.faculty.role.role_name != "Admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized."
        )

    return membership_exists


# FUNCTION FOR ONLY TEACHER ACCESS
async def teacher_access(
    institute_id: Annotated[int, Header(alias = "X-Institute-ID")],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    membership_exists = await get_current_user_institute_membership(
            db = db,
            current_user = current_user,
            institute_id = institute_id
        )
    
    if membership_exists is None or membership_exists.faculty.role.role_name != "Teacher":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized."
        )
    
    return membership_exists

