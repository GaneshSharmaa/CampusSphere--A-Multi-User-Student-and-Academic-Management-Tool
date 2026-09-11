# Importing the local module
from database.database import Base

# Importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, DateTime, Date, func, UniqueConstraint
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from institutes.models import Institute
    from programs.models import ProgramSubject

class Subject(Base):
    __tablename__ = "subjects"

    __table_args__ = (
        UniqueConstraint(
            "institute_id",
            "subject_code",
            name = "uq_subject_institute_code"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    subject_code: Mapped[str] = mapped_column(
        String(15),
        nullable = False,
        index = True
    )

    subject_name: Mapped[str] = mapped_column(
        String(50),
        nullable = False,
        index = True
    )

    institute_id: Mapped[int] = mapped_column(
        ForeignKey("institutes.id"),
        nullable = False,
        index = True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = func.now()),
        server_default = func.timezone("Asia/Kolkata", func.now()),
        nullable = False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone = func.now()),
        server_default = func.timezone("Asia/Kolkata", func.now()),
        onupdate = func.timezone("Asia/Kolkata", func.now()),
        nullable = False
    )

    # relationship to institute database model
    institute: Mapped["Institute"] = relationship(
        back_populates = "subjects"
    )

    # relationship to ProgramSubject database model
    program_subjects: Mapped[list["ProgramSubject"]] = relationship(
        back_populates = "subject"
    )

