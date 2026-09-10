# Importing the local modules
from database.database import Base

# Importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, DateTime, func, UniqueConstraint
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from users.models import User
    from institutes.models import Institute

# Creating the database model
class Membership(Base):
    __tablename__ = "memberships"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "institute_id",
            name="uq_user_institute"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
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

    # relationship to user database model
    user: Mapped["User"] = relationship(
        back_populates = "memberships"
    )

    # relationship to institute database model
    institute: Mapped["Institute"] = relationship(
        back_populates = "memberships"
    )

