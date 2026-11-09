# Importing the required modules
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Importing the Role database model, schemas
from roles.models import Role
from roles.schemas import RoleCreate, RoleResponse

# Importing the dependencies
from database.dependencies import get_db
from auth.dependencies import get_current_user_institute_membership, get_current_user

async def chk_role_exists(
    db: AsyncSession,
    role_name: str,
    institute_id: int
) -> Role | None:
    role_exists = await db.scalar(
        select(Role).where(
            Role.role_name == role_name,
            Role.institute_id == institute_id
        )
    )

    return role_exists


async def create_new_role(
    role_data: RoleCreate,
    institute_id: int,
    db: AsyncSession
) -> Role | None:
    existing_role = await chk_role_exists(
        db = db,
        role_name = role_data.role_name,
        institute_id = institute_id
    )

    if existing_role is not None:
        return None

    new_role = Role(
        **role_data.model_dump(),
        institute_id = institute_id
    )

    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)

    return new_role

