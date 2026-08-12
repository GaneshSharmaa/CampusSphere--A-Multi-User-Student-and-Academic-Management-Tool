# Importing required modules
from fastapi import FastAPI, HTTPException, status, Depends
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
from routes import users, faculty, roles, departments, students

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

# Include the `users` router
app.include_router(
    users.router,
    prefix = "/user",
    tags = ["User Management"]
)

# Include the `faculty` router
app.include_router(
    faculty.router,
    prefix = "/faculty",
    tags = ["Faculty Management"]
)

# Include the `roles` router
app.include_router(
    roles.router,
    prefix = "/role",
    tags = ["Role Management"]
)

# Include the `departments` router
app.include_router(
    departments.router,
    prefix = "/department",
    tags = ["Department Management"]
)

# Include the `students` router
app.include_router(
    students.router,
    prefix = "/student",
    tags = ["Student Management"]
)

# -------- HOME ROUTE --------
@app.get("/", include_in_schema = False)
async def home():
    return {
        "message": "Hello!"
    }

