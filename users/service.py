# Importing the User database model
from users.models import User

# Importing the required modules
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# Function to check if user exists or not
async def chk_user_exists(user_id: int, db: AsyncSession):
    user = select(User).where(user_id == User.id)

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )

    return user

