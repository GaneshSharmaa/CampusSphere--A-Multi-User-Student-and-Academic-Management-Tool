# Importing required modules
from fastapi import FastAPI, HTTPException, status, Depends
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Importing database dependencies
from database.database import engine
from database.dependencies import get_db

# Importing routes
from students import routes as student_routes
from departments import routes as department_routes
from users import routes as user_routes
from roles import routes as role_routes
from faculties import routes as faculty_routes
from institutes import routes as institute_routes

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
    user_routes.router,
    prefix = "/user",
    tags = ["User Management"]
)

# Include the `faculty` router
app.include_router(
    faculty_routes.router,
    prefix = "/faculty",
    tags = ["Faculty Management"]
)

# Include the `roles` router
app.include_router(
    role_routes.router,
    prefix = "/role",
    tags = ["Role Management"]
)

# Include the `departments` router
app.include_router(
    department_routes.router,
    prefix = "/department",
    tags = ["Department Management"]
)

# Include the `students` router
app.include_router(
    student_routes.router,
    prefix = "/student",
    tags = ["Student Management"]
)

# Include the `institute` router
app.include_router(
    institute_routes.router,
    prefix = "/institute",
    tags = ["Institute Management"]
)

# -------- HOME ROUTE --------
@app.get("/", include_in_schema = False)
async def home():
    return {
        "message": "Hello!"
    }

