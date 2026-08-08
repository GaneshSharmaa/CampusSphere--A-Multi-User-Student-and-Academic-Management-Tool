# importing local modules
from database.database import Base

# importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Sequence, DateTime, func
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.students import Student
    from models.faculty import Faculty

class Department(Base):
    __tablename__ = "departments"

    dept_code: Mapped[str] = mapped_column(
        String(10),
        primary_key = True,
        index = True
    )
    dept_name: Mapped[str] = mapped_column(
        String(50),
        unique = True,
        index = True,
        nullable = False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now(),
        nullable = False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        server_default = func.now(),
        onupdate = func.now(),
        nullable = False
    )

    # relationships
    students: Mapped[list["Student"]] = relationship(
        back_populates = "dept"
    )

    faculties: Mapped[list["Faculty"]] = relationship(
        back_populates = "dept"
    )

