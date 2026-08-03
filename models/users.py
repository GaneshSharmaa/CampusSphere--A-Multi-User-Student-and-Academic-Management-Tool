# importing the local modules
from database.database import Base

# importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, DateTime, Date, func
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.roles import Role

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True)
    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable = False
    )
    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable = False
    )
    dob: Mapped[date] = mapped_column(
        Date,
        nullable = False
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
        nullable = False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
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
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable = False,
        default = 1
    )

    # relationship
    role: Mapped["Role"] = relationship(
        back_populates = "users"
    )

