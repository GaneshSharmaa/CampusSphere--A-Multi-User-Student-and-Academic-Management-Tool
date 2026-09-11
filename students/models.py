# importing the local module
from database.database import Base
from faculties.models import SexEnum

# importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text, Integer, Sequence, Date, DateTime, func, Identity, CheckConstraint, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import User
    from departments.models import Department
    from institutes.models import Institute

class Student(Base):
    __tablename__ = "students"

    __table_args__ = (
        UniqueConstraint(
            "institute_id",
            "roll_no",
            name="uq_student_institute_roll_no"
        ),
        CheckConstraint(
            "start_batch_year >= 1970 AND start_batch_year <= 2100",
            name="ck_student_start_batch_year"
        ),
        CheckConstraint(
            "end_batch_year >= 1970 AND end_batch_year <= 2100",
            name="ck_student_end_batch_year"
        ),
        CheckConstraint(
            "end_batch_year >= start_batch_year",
            name="ck_student_batch_years"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    roll_no: Mapped[int] = mapped_column(
        nullable = False,
        index = True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique = True,
        nullable = False,
        index = True
    )

    first_name: Mapped[str] = mapped_column(
        String(25),
        nullable = False
    )

    last_name: Mapped[str] = mapped_column(
        String(25),
        nullable = False
    )

    dob: Mapped[date] = mapped_column(
        Date,
        nullable = False
    )

    sex: Mapped[SexEnum] = mapped_column(
        SQLEnum(SexEnum),
        nullable = False
    )

    address: Mapped[str] = mapped_column(
        Text,
        nullable = False
    )

    date_of_admission: Mapped[date] = mapped_column(
        Date,
        nullable = False
    )

    dept_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable = False,
        index = True
    )

    institute_id: Mapped[int] = mapped_column(
        ForeignKey("institutes.id"),
        nullable = False,
        index = True
    )

    start_batch_year: Mapped[int] = mapped_column(
        Integer,
        nullable = False
    )

    end_batch_year: Mapped[int] = mapped_column(
        Integer,
        nullable = False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.timezone("Asia/Kolkata", func.now()),
        nullable = False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.timezone("Asia/Kolkata", func.now()),
        onupdate = func.timezone("Asia/Kolkata", func.now()),
        nullable = False
    )

    # relationship to department database model
    department: Mapped["Department"] = relationship(
        back_populates = "students"
    )

    # relationship to institute database model
    institute: Mapped["Institute"] = relationship(
        back_populates = "students"
    )

    # relationship to user database model
    user: Mapped["User"] = relationship(
        back_populates = "student"
    )

