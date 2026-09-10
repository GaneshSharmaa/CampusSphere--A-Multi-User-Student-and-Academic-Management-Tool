# importing the local modules
from database.database import Base

# importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, DateTime, Date, func
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from students.models import Student
    from institutes.models import Institute
    from membership.models import Membership
    from faculties.models import Faculty

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key = True
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique = True,
        index = True,
        nullable = False
    )
    phone: Mapped[str] = mapped_column(
        String(15),
        index = True,
        nullable = False,
        unique = True
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
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

    # relationship to faculty database model
    faculty: Mapped["Faculty" | None] = relationship(
        back_populates = "user"
    )

    # relationship to student database model
    student: Mapped["User" | None] = relationship(
        back_populates = "user"
    )

    # relationship to membership database model
    memberships: Mapped[list["Membership"]] = relationship(
        back_populates = "user"
    )

