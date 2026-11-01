# Importing the required modules
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSesssion

# Importing the database models
from users.models import User
from departments.models import Department

async def check_department_exists(db: AsyncSesssion, current_user: User):
    dept_code_exists = await db.scalar(
        select(Department).options(
            selectinload(Department.institute)
        )
    )

