# Importing the local modules
from database.database import Base

# Importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, DateTime, Date, Time, func, CheckConstraint
from datetime import date, datetime, time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from faculties.models import Faculty
    from programs.models import Program
    from subjects.models import Subject

class Schedule(Base):
    __tablename__ = "schedules"

    __table_args__ = (
        CheckConstraint(
            "end_time > start_time",
            name = "ck_schedule_valid_time"
        ),
    )

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

    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("faculty.emp_id"),
        nullable = False,
        index = True
    )

    day_of_week: Mapped[str] = mapped_column(
        String(10),
        nullable = False
    )

    start_time: Mapped[time] = mapped_column(
        Time,
        nullable = False
    )

    end_time: Mapped[time] = mapped_column(
        Time,
        nullable = False
    )

    room: Mapped[str] = mapped_column(
        String(50),
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

    # relationship to program database model
    program: Mapped["Program"] = relationship(
        back_populates = "schedules"
    )

    # relationship to subject database model
    subject: Mapped["Subject"] = relationship(
        back_populates = "schedules"
    )

    # relationship to faculty database model
    faculty: Mapped["Faculty"] = relationship(
        back_populates = "schedules"
    )

