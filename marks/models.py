# Importing the local modules
from database.database import Base

# Importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Float, DateTime, Date, func, UniqueConstraint, CheckConstraint
from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from students.models import Student
    from subjects.models import Subject

class Mark(Base):
    __tablename__ = "marks"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "subject_id",
            "academic_year",
            name = "uq_student_subject_academic_year"
        ),
        CheckConstraint(
            "marks_obtained >= 0",
            name = "ck_marks_obtained_positive"
        ),
        CheckConstraint(
            "max_marks > 0",
            name = "ck_max_marks_positive"
        ),
        CheckConstraint(
            "marks_obtained <= max_marks",
            name = "ck_marks_not_exceed_max"
        ),
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

    academic_year: Mapped[str] = mapped_column(
        String(9),
        nullable = False,
        index = True
    )

    marks_obtained: Mapped[float] = mapped_column(
        Float,
        nullable = False
    )

    max_marks: Mapped[float] = mapped_column(
        Float,
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
        back_populates = "marks"
    )

    # relationship to subject database model
    subject: Mapped["Subject"] = relationship(
        back_populates = "marks"
    )

