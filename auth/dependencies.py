# Importing local module
from auth.jwt import verify_access_token
from database.dependencies import get_db
from roles.models import User
from faculties.models import Faculty

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
        select(User).options(selectinload(User.faculty).selectinload(Faculty.role)).where(User.id == user_id)
    )

    # Raising HTTP exception if not found
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Cannot validate the user"
        )

    return user

# Function to authorize `Admin` users only
async def admin_access(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.faculty.role.role_name == "Admin":
        return current_user

    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "Not authorized."
    )

# Function to authorize `Professor` users only
async def professor_access(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.faculty.role.role_name == "Professor":
        return current_user
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "Not authorized."
    )

# Function to authorize `HOD` users only
async def hod_access(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.faculty.role.role_name == "HOD":
        return current_user
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "Not authorized."
    )

# Function to authorize `Principal` users only
async def principal_access(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.faculty.role.role_name == "Principal":
        return current_user
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "Not authorized."
    )

# Function to authorize a list of roles
async def access(
    current_user: Annotated[User, Depends(get_current_user)],
    access: list
):
    if current_user.faculty.role.role_name in access:
        return current_user

    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "Not authorized."
    )

