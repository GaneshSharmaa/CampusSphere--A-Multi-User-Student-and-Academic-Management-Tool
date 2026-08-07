# importing required modules
from fastapi import FastAPI, HTTPException, status, Depends, Query
from fastapi.templating import Jinja2Templates
from typing import Annotated
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

# importing local modules
from database.database import engine
from database.dependencies import get_db
from models.users import User
from models.roles import Role
from schemas.users import UserCreate, UserResponse, UserLogin, UserQueryParams, UserUpdate
from schemas.token import Token
from auth.hashing import hash_password, verify_password
from auth.jwt import create_access_token
from auth.dependencies import get_current_user, require_access

# async database creation
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await engine.dispose()

# initializing the app
app = FastAPI(lifespan = lifespan)

# -------- HOME ROUTE --------
@app.get("/")
async def home():
    return {
        "message": "Hello!"
    }

# ------ REGISTER ROUTE - CREATING NEW USER ------
@app.post("/register", response_model = UserResponse)
async def create_new_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    email_chk = await db.scalar(select(User).where(user.email == User.email))

    if email_chk is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User with this email already exists!"
        )

    student_role = await db.scalar(
        select(Role).where(Role.role_name == "Student")
    )

    new_user = User(
        first_name = user.first_name,
        last_name = user.last_name,
        dob = user.dob,
        phone = user.phone,
        email = user.email,
        hashed_password = hash_password(user.password),
        role_id = student_role.id
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

# ------- LOGIN ROUTE - AUTHENTICATING USERS -------
@app.post("/login", response_model = Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await db.scalar(
        select(User).where(User.email == form_data.username)
    )

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password."
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password."
        )

    access_token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# --------- PROFILE ROUTE - SHOWS WHICH USER IS LOGGED IN ---------
@app.get("/me", response_model = UserResponse)
async def me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

# -------- DELETE ENDPOINT - ONLY ADMINS CAN DELETE THE USERS --------
@app.delete("/delete/user/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    access: Annotated[User, Depends(require_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await db.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )

    await db.delete(user)
    await db.commit()

# -------- GET USER INFORMATION ROUTE BY USER ID --------
@app.get("/user/{user_id}", response_model = UserResponse)
async def get_user(
    user_id: int,
    access: Annotated[User, Depends(require_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    user = await db.scalar(
        select(User).where(User.id == user_id)
    )

    if user is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )

    return user

# --------- FILTER USER ROUTE USING QUERY ROUTE ---------
@app.get("/users/search", response_model = list[UserResponse])
async def search_user(
    access: Annotated[User, Depends(require_access)],
    db: Annotated[AsyncSession, Depends(get_db)],
    q_params: Annotated[UserQueryParams, Query()]
):
    query = select(User)

    if q_params.first_name:
        query = query.where(User.first_name.ilike(f"%{q_params.first_name}%"))

    if q_params.last_name:
        query = query.where(User.last_name.ilike(f"%{q_params.last_name}%"))

    if q_params.email:
        query = query.where(User.email.ilike(f"%{q_params.email}%"))

    if q_params.phone:
        query = query.where(User.phone.ilike(f"%{q_params.phone}%"))

    if q_params.dob:
        query = query.where(User.dob.ilike(f"%{q_params.dob}%"))

    result = await db.scalars(query)
    users = result.all()

    return users

# ---------- PATCH ROUTE FOR UPDATING USER INFORMATION ----------
@app.patch("/me", response_model = UserResponse)
async def partial_user_update(
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    update_data = user_data.model_dump(exclude_unset = True)

    for key, value in update_data.items():
        setattr(current_user, key, value)

    await db.commit()
    await db.refresh(current_user)

    return current_user

# 