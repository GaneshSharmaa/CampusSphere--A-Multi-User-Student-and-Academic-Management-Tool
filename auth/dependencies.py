# Importing local module
from auth.jwt import verify_access_token
from database.dependencies import get_db
from users.models import User

# Importing the required module
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

oauth2scheme = OAuth2PasswordBearer(tokenUrl = "user/login")

# Function to get current user using token
async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2scheme)]
) -> User:
    # Verifying the access token and getting the payload
    payload = verify_access_token(token)

    # Converting the `sub` (user ID) to int
    user_id = int(payload["sub"])

    # Querying the database if user exists
    user = await db.scalar(
        select(User).where(User.id == user_id)
    )

    # Raising HTTP exception if not found
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Cannot validate the user."
        )

    return user

# Creating a dependency for getting the membership of the user
async def get_user_membership(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
) -> int:
    pass