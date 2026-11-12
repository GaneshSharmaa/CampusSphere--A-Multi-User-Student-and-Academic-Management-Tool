# Importing the required modules
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Importing the database models
from departments.models import Department
from departments.schemas import DeptQueryParam, CreateDepartment, UpdateDepartment, ResponseDepartment
from departments.exceptions import DepartmentNotFoundError, DuplicateDepartmentError


# Function to check whether the department exists or not
async def check_department_exists(
    db: AsyncSession,
    institute_id: int,
    department_data: DeptQueryParam,
    department_id: int | None = None,
):
    query = select(Department).where(
        Department.institute_id == institute_id,
        (Department.dept_code == department_data.dept_code)
        | (Department.dept_name == department_data.dept_name),
    )

    if department_id is not None:
        query = query.where(Department.id != department_id)

    return await db.scalar(query)


# Function to create deparment
async def create_new_department(
    db: AsyncSession,
    institute_id: int,
    department_data: CreateDepartment
):
    existing_department = await check_department_exists(
        db = db,
        institute_id = institute_id,
        department_data = department_data
    )

    if existing_department is not None:
        raise DuplicateDepartmentError("Department already exists.")

    new_department = Department(
        **department_data.model_dump(),
        institute_id = institute_id
    )

    db.add(new_department)
    await db.commit()
    await db.refresh(new_department)

    return new_department


# Function to search department
async def search_departments(
    db: AsyncSession,
    institute_id: int,
    params: DeptQueryParam
) -> list[Department]:
    query = select(Department).where(
        Department.institute_id == institute_id
    )

    if params.dept_code:
        query = query.where(
            Department.dept_code.ilike(f"%{params.dept_code}%")
        )

    if params.dept_name:
        query = query.where(
            Department.dept_name.ilike(f"%{params.dept_name}%")
        )

    result = await db.scalars(query)
    return list(result.all())


# Function to update the department info
async def update_department(
    db: AsyncSession,
    institute_id: int,
    department_id: int,
    department_data: UpdateDepartment
) -> Department:
    department = await db.scalar(
        select(Department).where(
            Department.institute_id == institute_id,
            Department.id == department_id
        )
    )

    if department is None:
        raise DepartmentNotFoundError("Department you're requesting to edit not found.")

    update_data = department_data.model_dump(
        exclude_unset = True
    )

    # Determine the final values after the update
    new_dept_code = update_data.get(
        "dept_code", department.dept_code
    )

    new_dept_name = update_data.get(
        "dept_name", department.dept_name
    )

    # Check duplicates, excluding the current department
    duplicate = await db.scalar(
        select(Department.id).where(
            Department.institute_id == institute_id,
            Department.id != department_id,
            ((Department.dept_code == new_dept_code)
             | (Department.dept_name == new_dept_name))
        )
    )

    if duplicate is not None:
        raise DuplicateDepartmentError(
            "The department information already exists."
        )

    for key, value in update_data.items():
        setattr(department, key, value)

    await db.commit()
    await db.refresh(department)

    return department


# Function to delete a department
async def delete_department(
    db: AsyncSession,
    institute_id: int,
    department_id: int
) -> None:
    department = await db.scalar(
        select(Department).where(
            Department.institute_id == institute_id,
            Department.id == department_id
        )
    )

    if department is None:
        raise DepartmentNotFoundError("Department not found")

    await db.delete(department)
    await db.commit()

