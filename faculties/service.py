from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from departments.models import Department
from faculties.exceptions import (
    DuplicateFacultyError,
    FacultyNotFoundError,
    FacultyReferenceNotFoundError,
)
from faculties.models import Faculty
from faculties.schemas import (
    FacultyCreate,
    FacultyQueryParams,
    FacultyUpdate,
)
from membership.models import Membership
from roles.models import Role
from users.models import User


# Check whether the faculty exists or not
async def chk_faculty_exists(
    db: AsyncSession,
    user_id: int,
    institute_id: int,
) -> Faculty | None:
    return await db.scalar(
        select(Faculty).where(
            Faculty.user_id == user_id,
            Faculty.institute_id == institute_id,
        )
    )


# Function to search a faculty
async def search_faculties(
    db: AsyncSession,
    institute_id: int,
    params: FacultyQueryParams,
) -> list[Faculty]:
    query = select(Faculty).where(Faculty.institute_id == institute_id)

    if params.user_id is not None:
        query = query.where(Faculty.user_id == params.user_id)
    if params.first_name is not None:
        query = query.where(Faculty.first_name.ilike(f"%{params.first_name}%"))
    if params.last_name is not None:
        query = query.where(Faculty.last_name.ilike(f"%{params.last_name}%"))
    if params.dob is not None:
        query = query.where(Faculty.dob == params.dob)
    if params.sex is not None:
        query = query.where(Faculty.sex == params.sex)
    if params.address is not None:
        query = query.where(Faculty.address.ilike(f"%{params.address}%"))
    if params.date_of_joining is not None:
        query = query.where(Faculty.date_of_joining == params.date_of_joining)
    if params.dept_code is not None:
        query = query.join(Faculty.department).where(
            Department.dept_code.ilike(f"%{params.dept_code}%")
        )
    if params.role_id is not None:
        query = query.where(Faculty.role_id == params.role_id)

    result = await db.scalars(query)
    return list(result.all())


# Function to add a faculty
async def add_faculty(
    db: AsyncSession,
    faculty: FacultyCreate,
    institute_id: int,
) -> Faculty:
    user_membership = await db.scalar(
        select(Membership).join(User, User.id == Membership.user_id).where(
            Membership.user_id == faculty.user_id,
            Membership.institute_id == institute_id,
        )
    )
    if user_membership is None:
        raise FacultyReferenceNotFoundError("User is not a member of this institute.")

    if await chk_faculty_exists(db, faculty.user_id, institute_id) is not None:
        raise DuplicateFacultyError("Faculty already exists.")

    department = await db.scalar(
        select(Department).where(
            Department.id == faculty.dept_id,
            Department.institute_id == institute_id,
        )
    )
    if department is None:
        raise FacultyReferenceNotFoundError("Department not found in this institute.")

    role = await db.scalar(
        select(Role).where(
            Role.id == faculty.role_id,
            Role.institute_id == institute_id,
        )
    )
    if role is None:
        raise FacultyReferenceNotFoundError("Role not found in this institute.")

    new_faculty = Faculty(
        **faculty.model_dump(),
        institute_id=institute_id,
    )

    db.add(new_faculty)
    await db.commit()
    await db.refresh(new_faculty)
    return new_faculty


# Function to update a faculty
async def update_faculty(
    db: AsyncSession,
    institute_id: int,
    emp_id: int,
    faculty_data: FacultyUpdate,
) -> Faculty:
    faculty = await db.scalar(
        select(Faculty).where(
            Faculty.emp_id == emp_id,
            Faculty.institute_id == institute_id,
        )
    )
    if faculty is None:
        raise FacultyNotFoundError("Faculty not found.")

    update_data = faculty_data.model_dump(exclude_unset=True)

    if "dept_id" in update_data:
        department = await db.scalar(
            select(Department).where(
                Department.id == update_data["dept_id"],
                Department.institute_id == institute_id,
            )
        )
        if department is None:
            raise FacultyReferenceNotFoundError("Department not found in this institute.")

    if "role_id" in update_data:
        role = await db.scalar(
            select(Role).where(
                Role.id == update_data["role_id"],
                Role.institute_id == institute_id,
            )
        )
        if role is None:
            raise FacultyReferenceNotFoundError("Role not found in this institute.")

    if "user_id" in update_data:
        membership = await db.scalar(
            select(Membership).where(
                Membership.user_id == update_data["user_id"],
                Membership.institute_id == institute_id,
            )
        )
        if membership is None:
            raise FacultyReferenceNotFoundError("User is not a member of this institute.")

        duplicate = await db.scalar(
            select(Faculty).where(
                Faculty.user_id == update_data["user_id"],
                Faculty.institute_id == institute_id,
                Faculty.emp_id != emp_id,
            )
        )
        if duplicate is not None:
            raise DuplicateFacultyError("Faculty already exists.")

    for key, value in update_data.items():
        setattr(faculty, key, value)

    await db.commit()
    await db.refresh(faculty)
    return faculty


# Function for deleting a faculty
async def delete_faculty(
    db: AsyncSession,
    institute_id: int,
    emp_id: int,
) -> None:
    faculty = await db.scalar(
        select(Faculty).where(
            Faculty.emp_id == emp_id,
            Faculty.institute_id == institute_id,
        )
    )
    if faculty is None:
        raise FacultyNotFoundError("Faculty not found.")

    await db.delete(faculty)
    await db.commit()

