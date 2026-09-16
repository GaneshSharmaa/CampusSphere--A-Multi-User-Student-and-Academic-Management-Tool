# Importing the local modules
from database.database import Base

# Importing the required modules
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Numeric, Integer, DateTime, Date, func, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from faculties.models import Faculty

# Creating a salary status enum — pending / paid
class SalaryStatus(Enum):
    PENDING = "Pending"
    PAID = "Paid"

# Creating the database model
class Salary(Base):
    __tablename__ = "salaries"

    __table_args__ = (
        UniqueConstraint(
            "faculty_id",
            "salary_month",
            name = "uq_faculty_salary_month"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key = True,
        index = True
    )

    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("faculty.emp_id"),
        nullable = False,
        index = True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable = False
    )

    salary_month: Mapped[date] = mapped_column(
        Date,
        nullable = False
    )

    status: Mapped[SalaryStatus] = mapped_column(
        SQLEnum(SalaryStatus),
        nullable = False,
        default = SalaryStatus.PENDING
    )

    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone = True),
        nullable = True
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
    faculty: Mapped["Faculty"] = relationship(
        back_populates = "salaries"
    )

