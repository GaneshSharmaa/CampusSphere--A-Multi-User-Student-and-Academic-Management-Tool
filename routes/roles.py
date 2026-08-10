# Importing the required modules
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Annotated

# Importing the database models
from models.roles import Role
from models.users import User

# Importing the database dependencies
from database.dependencies import get_db

# Importing the schemas
from schemas.roles import RoleCreate, RoleResponse

# Importing the authentication and authorization modules
from auth.dependencies import get_current_user, admin_access

router = APIRouter()

# ------- POST ROUTE - CREATING ROLE ROUTE -------
@router.post("/create-role", response_model = RoleResponse)
async def create_role(
    role: RoleCreate,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    role_chk = await db.scalar(
        select(Role).where(Role.role_name == role.role_name)
    )

    if role_chk is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Role already exists."
        )

    new_role = Role(**role.model_dump())

    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)

