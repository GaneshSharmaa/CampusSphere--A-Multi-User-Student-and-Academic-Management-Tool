# importing required modules
from fastapi import FastAPI, HTTPException, status, Depends
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
from schemas.users import UserCreate, UserResponse, UserLogin
from schemas.token import Token
from auth.hashing import hash_password, verify_password
from auth.jwt import create_access_token
from auth.dependencies import get_current_user

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

    new_user = User(
        first_name = user.first_name,
        last_name = user.last_name,
        dob = user.dob,
        phone = user.phone,
        email = user.email,
        hashed_password = hash_password(user.password)
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

@app.get("/me")
async def me(current_user = Depends(get_current_user)):
    return current_user
