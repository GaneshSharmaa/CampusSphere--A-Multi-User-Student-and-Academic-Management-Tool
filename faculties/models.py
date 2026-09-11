# importing local modules
from database.database import Base

# importing required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text, Integer, DateTime, Date, func, Identity
from sqlalchemy import Enum as SQLEnum
from datetime import datetime, date
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from roles.models import Role
    from departments.models import Department
    from users.models import User
    from institutes.models import Institute

class SexEnum(Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class Faculty(Base):
    __tablename__ = "faculty"

    emp_id: Mapped[int] = mapped_column(
        primary_key = True,
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

    date_of_joining: Mapped[date] = mapped_column(
        Date,
        nullable = False
    )

    dept_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable = False,
        index = True
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable = False,
        index = True
    )

    institute_id: Mapped[int] = mapped_column(
        ForeignKey("institutes.id"),
        nullable = False,
        index = True
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

    # relationship to user database model
    user: Mapped["User"] = relationship(
        back_populates = "faculty"
    )

    # relationship to role database model
    role: Mapped["Role"] = relationship(
        back_populates = "faculties"
    )

    # relationship to department database model
    department: Mapped["Department"] = relationship(
        back_populates = "faculties"
    )

    # relationship to institute database model
    institute: Mapped["Institute"] = relationship(
        back_populates = "faculties"
    )

