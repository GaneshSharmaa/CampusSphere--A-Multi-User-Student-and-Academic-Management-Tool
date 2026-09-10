# Importing the local modules
from database.database import Base

# Importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Text, Date, DateTime, func
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from departments.models import Department
    from students.models import Student
    from faculties.models import Faculty
    from membership.models import Membership
    from roles.models import Role
    from programs.models import Program

class Institute(Base):
    __tablename__ = "institutes"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )
    institute_code: Mapped[str] = mapped_column(
        String(6),
        index = True,
        nullable = False,
        unique = True
    )
    institute_name: Mapped[str] = mapped_column(
        Text,
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

    # relationship to membership database model
    memberships: Mapped[list["Membership"]] = relationship(
        back_populates = "institute"
    )

    # relationship to roles database model
    roles: Mapped[list["Role"]] = relationship(
        back_populates = "institute"
    )

    # relationship to department database model
    departments: Mapped[list["Department"]] = relationship(
        back_populates = "institute"
    )

    # relationship to student database model
    students: Mapped[list["Student"]] = relationship(
        back_populates = "institute"
    )

    # relationship to faculty database model
    faculties: Mapped[list["Faculty"]] = relationship(
        back_populates = "institute"
    )

    # relationship to program database model
    programs: Mapped[list["Program"]] = relationship(
        back_populates = "institute"
    )

