# Importing the local modules
from database.database import Base

# Importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, Integer, DateTime, Date, func, UniqueConstraint
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from students.models import Student
    from subjects.models import Subject

class Attendance(Base):
    __tablename__ = "attendance"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "subject_id",
            "attendance_date",
            name = "uq_student_subject_attendance_date"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"),
        nullable = False,
        index = True
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"),
        nullable = False,
        index = True
    )

    attendance_date: Mapped[date] = mapped_column(
        Date,
        nullable = False,
        index = True
    )

    is_present: Mapped[bool] = mapped_column(
        Boolean,
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

    # relationship to student database model
    student: Mapped["Student"] = relationship(
        back_populates="attendance"
    )

    # relationship to subject database model
    subject: Mapped["Subject"] = relationship(
        back_populates="attendance"
    )

