# Importing the required modules
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Annotated

# Importing the database models
from roles.models import Role
from users.models import User
from membership.models import Membership

# Importing the database dependencies
from database.dependencies import get_db

# Importing the schemas
from roles.schemas import RoleCreate, RoleResponse

# Importing the authentication and authorization modules
from auth.dependencies import get_current_user_institute_membership
from auth.role_based_access import admin_access
from roles.service import chk_role_exists, create_new_role

router = APIRouter()

# ------- POST ROUTE - CREATING ROLE ROUTE -------
@router.post("/create", response_model = RoleResponse)
async def create_role(
    db: Annotated[AsyncSession, Depends(get_db)],
    role: RoleCreate,
    access: Annotated[Membership, Depends(admin_access)],
    institute: Annotated[Membership, Depends(get_current_user_institute_membership)]
):
    role_exists_chk = await chk_role_exists

    if role_exists_chk is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "The role already exists."
        )

    new_role = await create_new_role(
        db = db,
        institute_id = access.institute_id,
        role_data = role
    )

    return new_role

