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

    # relationships
    students: Mapped[list["Student"]] = relationship(
        back_populates = "institutes"
    )

