# Import the required modules
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Importing the database models
from users.models import User
from students.models import Student
from membership.models import Membership
from departments.models import Department
from faculties.models import Faculty
from programs.models import Program

# Importing the schemas
from students.schemas import StudentCreate, StudentQueryParams, StudentResponse, StudentUpdate


async def get_user_institute_id(
    db: AsyncSession,
    current_user: User
) -> int:
    faculty_institute_id = await db.scalar(
        select(Faculty.institute_id).where(Faculty.user_id == current_user.id)
    )
    if faculty_institute_id is not None:
        return faculty_institute_id

    institute_ids = (
        await db.scalars(
            select(Membership.institute_id)
            .where(Membership.user_id == current_user.id)
            .order_by(Membership.id)
        )
    ).all()
    if len(institute_ids) != 1:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "User must belong to exactly one institute.",
        )

    return institute_ids[0]

# ----- For fetching the students using query parameters -----
async def search_student(
    db: AsyncSession,
    param: StudentQueryParams,
    current_user: User
) -> list[Student]:
    institute_id = await get_user_institute_id(db, current_user)

    # Check if current logged in user is in student table
    student_chk = await db.scalar(
        select(Student).where(
            Student.user_id == current_user.id
        )
    )

    # If yes, raise HTTP exception
    if student_chk is not None:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Not authorized."
        )

    # Query
    query = select(Student).where(Student.institute_id == institute_id)

    # Query parameters
    if param.first_name is not None:
        query = query.where(
            Student.first_name.ilike(f"%{param.first_name}%")
        )
    if param.last_name is not None:
        query = query.where(
            Student.last_name.ilike(f"%{param.last_name}%")
        )
    if param.dob is not None:
        query = query.where(
            Student.dob == param.dob
        )
    if param.sex is not None:
        query = query.where(
            Student.sex == param.sex
        )
    if param.address is not None:
        query = query.where(
            Student.address.ilike(f"%{param.address}%")
        )
    if param.date_of_admission is not None:
        query = query.where(
            Student.date_of_admission == param.date_of_admission
        )
    if param.dept_code is not None:
        query = query.join(Student.department).where(
            Department.dept_code.ilike(f"%{param.dept_code}%")
        )
    if param.start_batch_year is not None:
        query = query.where(
            Student.start_batch_year == param.start_batch_year
        )
    if param.end_batch_year is not None:
        query = query.where(
            Student.end_batch_year == param.end_batch_year
        )

    result = await db.scalars(query)
    students = result.all()
    return students

# ----- For creating a student (admin accessed only) -----
async def create_new_student(
    db: AsyncSession,
    student_data: StudentCreate,
    current_user: User
) -> Student:
    institute_id = await get_user_institute_id(db, current_user)

    user_exists = await db.scalar(
        select(User)
        .join(Membership, Membership.user_id == User.id)
        .where(
            User.id == student_data.user_id,
            Membership.institute_id == institute_id,
        )
    )

    if user_exists is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )

    student_exists = await db.scalar(select(Student).where(
        Student.user_id == student_data.user_id,
        Student.institute_id == institute_id,
    ))

    if student_exists is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Student already exists."
        )

    department = await db.scalar(select(Department).where(
        Department.dept_code == student_data.dept_code,
        Department.institute_id == institute_id,
    ))
    if department is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Department not found in the current institute.",
        )

    program = await db.scalar(select(Program).where(
        Program.id == student_data.program_id,
        Program.institute_id == institute_id,
        Program.department_id == department.id,
    ))
    if program is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Program not found in the current department and institute.",
        )

    student = Student(
        **student_data.model_dump(exclude={"dept_code"}),
        dept_id = department.id,
        institute_id = institute_id,
    )

    db.add(student)

    await db.commit()
    await db.refresh(student)

    return student

# --------- For updating the existing student ---------
async def update_student(
    db: AsyncSession,
    student_id: int,
    student_data: StudentUpdate,
    current_user: User
) -> Student:
    institute_id = await get_user_institute_id(db, current_user)

    # Check if student with student_id exists
    student = await db.scalar(
        select(Student).where(
            Student.id == student_id,
            Student.institute_id == institute_id,
        )
    )
    
    # If no, raise HTTP exception
    if student is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Student doesn't exists."
        )

    update_data = student_data.model_dump(exclude_unset=True)
    if "dept_code" in update_data:
        department = await db.scalar(select(Department).where(
            Department.dept_code == update_data.pop("dept_code"),
            Department.institute_id == institute_id,
        ))
        if department is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found in the current institute.",
            )
        update_data["dept_id"] = department.id

    for key, value in update_data.items():
        setattr(student, key, value)

    db.add(student)
    await db.commit()
    await db.refresh(student)

    return student

# ------------- For deleting the student -------------
async def delete_student(
    db: AsyncSession,
    student_id: int,
    current_user: User
) -> None:
    institute_id = await get_user_institute_id(db, current_user)

    # Check if student with student_id exists
    student = await db.scalar(
        select(Student).where(
            Student.id == student_id,
            Student.institute_id == institute_id,
        )
    )

    # If no, raise HTTP exception
    if student is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Student not found."
        )

    await db.delete(student)
    await db.commit()

