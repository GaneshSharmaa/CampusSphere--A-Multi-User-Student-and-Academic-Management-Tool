# importing the local modules
from database.database import Base

# importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from roles.models import User
    from faculties.models import Faculty

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        primary_key = True
    )
    role_name: Mapped[str] = mapped_column(
        String(30),
        unique = True,
        nullable = False
    )

    # relationships
    faculties: Mapped[list["Faculty"]] = relationship(
        back_populates = "role"
    )
    
