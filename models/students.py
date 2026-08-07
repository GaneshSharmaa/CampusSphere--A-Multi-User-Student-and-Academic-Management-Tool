# importing the local module
from database.database import Base

# importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Sequence, Date, DateTime, func, Identity
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.users import User
    from.departments import Department

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
    dept_code: Mapped[str] = mapped_column(
        ForeignKey("departments.dept_code"),
        nullable = False
    )
    admission_date: Mapped[date] = mapped_column(
        Date,
        nullable = False
    )

    user: Mapped["User"] = relationship(
        back_populates = "student"
    )

    department: Mapped["Department"] = relationship(
        back_populates = "students"
    )

