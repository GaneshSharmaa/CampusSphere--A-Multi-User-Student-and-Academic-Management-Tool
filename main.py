# Importing required modules
from fastapi import FastAPI, HTTPException, status, Depends
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Importing database dependencies
from database.database import engine
from database.dependencies import get_db

# Importing database models
from departments import routes
from departments.models import Department
from faculties.models import Faculty
from faculties import routes
from roles import routes
from users.models import Role
from students.models import Student
from roles.models import User

# Importing schemas
from faculties.schemas import FacultyCreate, FacultyResponse
from roles.schemas import RoleCreate, RoleResponse

# Importing authentication and authorization modules
from auth.dependencies import get_current_user, admin_access, professor_access, hod_access, principal_access

# Importing routes
from students import routes
from departments import routes
from users import routes
from roles import routes
from faculties import routes

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
    routes.router,
    prefix = "/user",
    tags = ["User Management"]
)

# Include the `faculty` router
app.include_router(
    routes.router,
    prefix = "/faculty",
    tags = ["Faculty Management"]
)

# Include the `roles` router
app.include_router(
    routes.router,
    prefix = "/role",
    tags = ["Role Management"]
)

# Include the `departments` router
app.include_router(
    routes.router,
    prefix = "/department",
    tags = ["Department Management"]
)

# Include the `students` router
app.include_router(
    routes.router,
    prefix = "/student",
    tags = ["Student Management"]
)

# -------- HOME ROUTE --------
@app.get("/", include_in_schema = False)
async def home():
    return {
        "message": "Hello!"
    }

