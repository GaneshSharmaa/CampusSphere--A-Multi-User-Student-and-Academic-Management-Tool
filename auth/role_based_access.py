from typing import Annotated
from fastapi import HTTPException, status, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies import get_current_user, get_current_user_institute_membership
from database.dependencies import get_db
from membership.models import Membership

# FUNCTION FOR ONLY ADMIN ACCESS
async def admin_access(
    membership: Annotated[Membership, Depends(get_current_user_institute_membership)]
) -> int:
    if (membership.role is None or membership.role.role_name != "Admin"):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized."
        )

    return membership.institute_id


# FUNCTION FOR ONLY TEACHER ACCESS
async def teacher_access(
    membership: Annotated[Membership, Depends(get_current_user_institute_membership)]
):
    if (membership.role is None or membership.role.role_name != "Teacher"):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized."
        )

    return membership.institute_id

