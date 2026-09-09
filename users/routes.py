# Importing the required modules
from fastapi import HTTPException, status, Depends, Query, APIRouter
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi.security import OAuth2PasswordRequestForm

# Importing the database dependencies
from database.dependencies import get_db

# Importing the database models
from roles.models import User

# Importing the schemas
from users.schemas import UserCreate, UserResponse, UserQueryParams
from auth.schemas import Token

# Importing authentication and authorization modules
from auth.hashing import hash_password, verify_password
from auth.jwt import create_access_token
from auth.dependencies import get_current_user, admin_access, professor_access, hod_access, principal_access

router = APIRouter()

# ------ REGISTER ROUTE - CREATING NEW USER ------
@router.post("/register", response_model = UserResponse)
async def create_new_user(
    user: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Checking if user with this email exists
    email_chk = await db.scalar(
        select(User).where(user.email == User.email)
    )

    # Checking if user with this phone exists
    phone_chk = await db.scalar(
        select(User).where(User.phone == user.phone)
    )

    # If email already exists raise HTTP exception
    if email_chk is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User with this email already exists!"
        )

    # If phone already exists raise HTTP exception
    if phone_chk is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User with this phone already exists!"
        )

    # Setting the variable to enter in database
    new_user = User(
        email = user.email,
        phone = user.phone,
        hashed_password = hash_password(user.password)
    )

    # Adding and commiting the changes
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

# ------- LOGIN ROUTE - AUTHENTICATING USERS -------
@router.post("/login", response_model = Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Checking if user with this email exists
    user = await db.scalar(
        select(User).where(User.email == form_data.username)
    )

    # If not exists, then raise HTTP exception
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password."
        )

    # Verifying password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password."
        )

    # Creating access token
    access_token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ---------- GET USER ROUTE ----------
@router.get("/me", response_model = UserResponse)
async def my_profile(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user

# -------- GET USER ROUTE (QUERY PARAMETER) --------
@router.get("/search", response_model = list[UserResponse])
async def get_user_info(
    user: Annotated[UserQueryParams, Query()],
    admin_access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    statement = select(User)

    if user.email:
        statement = statement.where(User.email.ilike(f"%{user.email}%"))
    if user.phone:
        statement = statement.where(User.phone.ilike(f"%{user.phone}%"))

    result = await db.scalars(statement)
    users = result.all()
    return users

