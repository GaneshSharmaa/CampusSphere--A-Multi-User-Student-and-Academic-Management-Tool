from typing import Annotated
from fastapi import HTTPException, status, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies import get_current_user, get_current_user_institute_membership
from membership.models import Membership


# Function for creating role-based access
def require_role(*required_role: str):
    async def role_checker(
        membership: Annotated[Membership, Depends(get_current_user_institute_membership)]
    ) -> Membership:
        if (membership.role is None or membership.role.role_name not in required_role):
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "Not authorized."
            )

        return membership
    return role_checker


# Admin access
require_admin = require_role("Admin")
# Principal access
require_principal = require_role("Principal")

