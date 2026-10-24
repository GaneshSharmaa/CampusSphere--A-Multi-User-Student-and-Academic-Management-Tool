# Importing the required modules
from fastapi import HTTPException, status, Depends, Query, APIRouter
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from fastapi.security import OAuth2PasswordRequestForm

# Importing the database dependencies
from database.dependencies import get_db

# Importing the database models
from users.models import User
from institutes.models import Institute
from membership.models import Membership

# Importing the schemas
from users.schemas import UserCreate, UserResponse, UserQueryParams
from auth.schemas import Token, InstituteSummary

# Importing authentication and authorization modules
from auth.hashing import hash_password, verify_password
from auth.jwt import create_access_token
from auth.dependencies import get_current_user

router = APIRouter()

# ------ REGISTER ROUTE - CREATING NEW USER ------
@router.post("/register", response_model = UserResponse)
async def create_new_user(
    user: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Checking if user with this email exists
    email_chk = await db.scalar(
        select(User).where(User.email == user.email)
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

# ------------ Getting the list of all institutes ------------
@router.get("/me/institutes", response_model = list[InstituteSummary])
async def get_all_institutes(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    memberships = await db.scalars(
        select(Institute).join(Membership).where(
            Membership.user_id == current_user.id
        )
    )

    return memberships.all()

# -------- Selecting an active institute --------
@router.post("/me/active-institute", response_model = Token)
async def active_institute(
    institute_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    membership = await db.scalar(
        select(Membership).where(
            Membership.user_id == current_user.id,
            Membership.institute_id == institute_id
        )
    )

    if membership is None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized."
        )

    new_token = create_access_token(
        data = {
            "sub": str(current_user.id),
            "institute_id": str(institute_id)
        }
    )

    return {
        "access_token": new_token,
        "token_type": "bearer"
    }

# -------- GET USER ROUTE (QUERY PARAMETER) --------
@router.get("/search", response_model = list[UserResponse])
async def get_user_info(
    user: Annotated[UserQueryParams, Query()],
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

