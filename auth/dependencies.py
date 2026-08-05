# importing local module
from auth.jwt import verify_access_token
from database.dependencies import get_db
from models.users import User
from models.roles import Role

# importing the required module
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

oauth2scheme = OAuth2PasswordBearer(tokenUrl = "login")

# function to get current user using token
async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2scheme)]
) -> User:
    # verifying the access token and getting the payload
    payload = verify_access_token(token)

    # converting the `sub` (user ID) to int
    user_id = int(payload["sub"])

    # querying the database if user exists
    user = await db.scalar(
        select(User).options(selectinload(User.role)).where(User.id == user_id)
    )

    # raising HTTP exception if not found
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Cannot validate the user"
        )

    return user

# function to authorize only admin and teacher user
async def require_access(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role.role_name == "Admin" or current_user.role.role_name == "Teacher":
        return current_user

    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = "Not authorized."
    )

