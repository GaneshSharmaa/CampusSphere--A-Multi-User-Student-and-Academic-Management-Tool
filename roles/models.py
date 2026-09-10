# importing the local modules
from database.database import Base

# importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from faculties.models import Faculty
    from institutes.models import Institute

class Role(Base):
    __tablename__ = "roles"

    __table_args__ = (
        UniqueConstraint(
            "institute_id",
            "role_name",
            name="uq_role_institute_name"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    role_name: Mapped[str] = mapped_column(
        String(30),
        nullable = False
    )

    institute_id: Mapped[int] = mapped_column(
        ForeignKey("institutes.id"),
        nullable = False,
        index = True
    )

    # relationship to faculty database model
    faculties: Mapped[list["Faculty"]] = relationship(
        back_populates = "role"
    )
    
    # relationship to institute database model
    institute: Mapped["Institute"] = relationship(
        back_populates="roles"
    )

