# importing local module
from auth.jwt import verify_access_token
from database.dependencies import get_db
from models.users import User
from models.roles import Role

# importing the required module
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

oauth2scheme = OAuth2PasswordBearer(tokenUrl = "login")

async def get_user_current(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2scheme)]
) -> User:
    # verifying the access token and getting the payload
    payload = verify_access_token(token)

    # converting the `sub` (user ID) to int
    user_id = int(payload["sub"])

    # querying the database if user exists
    user = await db.scalar(
        select(User).where(User.id == user_id)
    )

    # raising HTTP exception if not found
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Cannot validate the user"
        )

    return user
