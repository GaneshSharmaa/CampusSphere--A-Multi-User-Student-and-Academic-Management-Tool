# importing required modules
from fastapi import FastAPI, HTTPException, status, Depends, Query
from typing import Annotated
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

# importing database related local modules
from database.database import engine
from database.dependencies import get_db

# importing local database models
from models.departments import Department
from models.faculty import Faculty
from models.roles import Role
from models.students import Student
from models.users import User

# importing local schemas
from schemas.users import UserCreate, UserResponse, UserLogin
from schemas.token import Token
from schemas.departments import CreateDepartment, ResponseDepartment
from schemas.faculty import FacultyCreate, FacultyResponse
from schemas.roles import RoleCreate, RoleResponse

# importing authentication and authorization local modules
from auth.hashing import hash_password, verify_password
from auth.jwt import create_access_token
from auth.dependencies import get_current_user, admin_access, professor_access, hod_access, principal_access

# async database creation
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await engine.dispose()

# initializing the app
app = FastAPI(lifespan = lifespan, title = "CampusSphere: A Multi-User Student and Academic Management Tool")

# -------- HOME ROUTE --------
@app.get("/")
async def home():
    return {
        "message": "Hello!"
    }

# ------ REGISTER ROUTE - CREATING NEW USER ------
@app.post("/register", response_model = UserResponse)
async def create_new_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    email_chk = await db.scalar(
        select(User).where(user.email == User.email)
    )

    phone_chk = await db.scalar(
        select(User).where(User.phone == user.phone)
    )

    if email_chk is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User with this email already exists!"
        )
    
    if phone_chk is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User with this phone already exists!"
        )

    new_user = User(
        email = user.email,
        phone = user.phone,
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

# --------- CREATING ROLE ROUTE ---------
@app.post("/create-role", response_model = RoleResponse)
async def create_role(
    role: RoleCreate,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    role_chk = await db.scalar(
        select(Role).where(Role.role_name == role.role_name)
    )

    if role_chk is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Role already exists."
        )

    db.add(role)
    await db.commit()
    await db.refresh(role)

# CREATING FACULTY ROUTE
@app.post("/create-faculty", response_model = FacultyResponse)
async def create_faculty(
    faculty: FacultyCreate,
    access: Annotated[User, Depends(admin_access)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    faculty_exists = await db.scalar(
        select(Faculty).where(Faculty.user_id == faculty.user_id)
    )

    if faculty_exists is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Faculty already exists."
        )

    user_exists = await db.scalar(
        select(User).where(User.id == faculty.user_id)
    )

    if user_exists is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )

    faculty_detail = Faculty(
        user_id = faculty.user_id,
        first_name = faculty.first_name,
        last_name = faculty.last_name,
        dob = faculty.dob,
        sex = faculty.sex,
        address = faculty.address,
        date_of_joining = faculty.date_of_joining,
        dept_code = faculty.dept_code,
        role_id = faculty.role_id,
    )

    db.add(faculty_detail)
    await db.commit()
    await db.refresh(faculty_detail)

    return faculty_detail

