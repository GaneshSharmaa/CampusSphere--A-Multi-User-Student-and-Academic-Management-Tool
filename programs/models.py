# importing the local modules
from database.database import Base

# importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, DateTime, Date, func, UniqueConstraint, CheckConstraint
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from departments.models import Department
    from institutes.models import Institute
    from students.models import Student
    from subjects.models import Subject

class Program(Base):
    __tablename__ = "programs"

    __table_args__ = (
        UniqueConstraint(
            "institute_id",
            "program_code",
            name = "uq_program_institute_code"
        ),
        CheckConstraint(
            "duration_years > 0",
            name = "ck_program_duration"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    program_code: Mapped[str] = mapped_column(
        String(15),
        nullable = False,
        index = True
    )

    program_name: Mapped[str] = mapped_column(
        String(100),
        nullable = False
    )

    degree: Mapped[str] = mapped_column(
        String(30),
        nullable = False
    )

    duration_years: Mapped[int] = mapped_column(
        Integer,
        nullable = False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
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

    # relationship to department database model
    department: Mapped["Department"] = relationship(
        back_populates = "programs"
    )

    # relationship to institute database model
    institute: Mapped["Institute"] = relationship(
        back_populates = "programs"
    )

    # relationship to student database model
    students: Mapped[list["Student"]] = relationship(
        back_populates = "program"
    )

    # relationship to ProgramSubject database model
    program_subjects: Mapped[list["ProgramSubject"]] = relationship(
        back_populates = "program"
    )

class ProgramSubject(Base):
    __tablename__ = "program_subjects"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    program_id: Mapped[int] = mapped_column(
        ForeignKey("programs.id"),
        nullable = False,
        index = True
    )

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id"),
        nullable = False,
        index = True
    )

    semester: Mapped[int] = mapped_column(
        Integer,
        nullable = False
    )

    credits: Mapped[int] = mapped_column(
        Integer,
        nullable = False
    )

    is_elective: Mapped[bool] = mapped_column(
        Boolean,
        default = False,
        nullable = False
    )

    __table_args__ = (
        UniqueConstraint(
            "program_id",
            "subject_id",
            name = "uq_program_subject"
        ),
    )

    program: Mapped["Program"] = relationship(
        back_populates = "program_subjects"
    )

    subject: Mapped["Subject"] = relationship(
        back_populates = "program_subjects"
    )

