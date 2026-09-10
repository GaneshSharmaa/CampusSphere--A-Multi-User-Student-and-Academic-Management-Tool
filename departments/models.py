# importing local modules
from database.database import Base

# importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Sequence, DateTime, func, UniqueConstraint
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from students.models import Student
    from faculties.models import Faculty
    from institutes.models import Institute

class Department(Base):
    __tablename__ = "departments"

    __table_args__ = (
        UniqueConstraint(
            "institute_id",
            "dept_code",
            name = "uq_department_institute_code"
        )
    )

    id: Mapped[int] = mapped_column(
        primary_key = True,
        nullable = False,
        index = True
    )

    dept_code: Mapped[str] = mapped_column(
        String(10),
        nullable = False,
        index = True
    )

    dept_name: Mapped[str] = mapped_column(
        String(50),
        unique = True,
        index = True,
        nullable = False
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

    # relationship to faculty database model
    faculties: Mapped[list["Faculty"]] = relationship(
        back_populates = "department"
    )

    # relationship to student database model
    students: Mapped[list["Student"]] = relationship(
        back_populates = "department"
    )

    # relationship to institute database model
    institute: Mapped["Institute"] = relationship(
        back_populates = "departments"
    )

