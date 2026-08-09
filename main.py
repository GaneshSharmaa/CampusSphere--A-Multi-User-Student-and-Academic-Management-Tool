# Importing required modules
from fastapi import FastAPI, HTTPException, status, Depends, Query
from typing import Annotated
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Importing database dependencies
from database.database import engine
from database.dependencies import get_db

# Importing database models
from models.departments import Department
from models.faculty import Faculty
from models.roles import Role
from models.students import Student
from models.users import User

# Importing schemas
from schemas.faculty import FacultyCreate, FacultyResponse
from schemas.roles import RoleCreate, RoleResponse

# Importing authentication and authorization modules
from auth.dependencies import get_current_user, admin_access, professor_access, hod_access, principal_access

# Importing routes
from routes import users

# Async database creation
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await engine.dispose()

# Initializing the app
app = FastAPI(
    title = "CampusSphere: A Multi-User Student and Academic Management Tool",
    lifespan = lifespan
)

# Include the `Auth` router
app.include_router(
    users.router,
    prefix = "/users",
    tags = ["User Management"]
)

# -------- HOME ROUTE --------
@app.get("/")
async def home():
    return {
        "message": "Hello!"
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

# --------- CREATING FACULTY ROUTE ---------
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

