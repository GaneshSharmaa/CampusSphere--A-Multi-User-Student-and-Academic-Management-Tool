# importing the local module
from database.database import Base
from faculties.models import SexEnum

# importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text, Integer, Sequence, Date, DateTime, func, Identity, CheckConstraint
from sqlalchemy import Enum as SQLEnum
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from roles.models import User
    from departments.models import Department

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )
    roll_no: Mapped[int] = mapped_column(
        Identity(start = 1001),
        unique = True,
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
    dept_code: Mapped[str] = mapped_column(
        ForeignKey("departments.dept_code"),
        nullable = False
    )
    start_batch_year: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("start_batch_year >= 1970 AND start_batch_year <= 2100"),
        nullable = False
    )
    end_batch_year: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("end_batch_year >= 1970 AND end_batch_year <= 2100"),
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
        server_onupdate = func.timezone("Asia/Kolkata", func.now()),
        nullable = False
    )

    # relationships
    dept: Mapped["Department"] = relationship(
        back_populates = "students"
    )

