# Importing the local modules
from database.database import Base

# Importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Numeric, DateTime, Date, func, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from datetime import datetime, date
from enum import Enum
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from students.models import Student

# Enum for Fee Status — Pending or Paid
class FeeStatus(Enum):
    PENDING = "Pending"
    PAID = "Paid"

# The database model
class Fee(Base):
    __tablename__ = "fees"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"),
        nullable = False,
        index = True
    )

    fee_type: Mapped[str] = mapped_column(
        String(30),
        nullable = False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )

    due_date: Mapped[date] = mapped_column(
        Date,
        nullable = False
    )

    status: Mapped[FeeStatus] = mapped_column(
        SQLEnum(FeeStatus),
        nullable = False,
        default = FeeStatus.PENDING
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone = True),
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
        back_populates="fees"
    )

