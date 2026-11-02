# Importing the required modules
import secrets, string
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Importing the database model
from institutes.models import Institute

# Importing the database dependencies
from database.dependencies import get_db

# ------ FUNCTION FOR GENERATING UNIQUE CODES ------
async def generate_code(
    db: AsyncSession
):
    ALPHABETS = list(string.ascii_uppercase)
    NUMBERS = list(string.digits)

    while True:
        list_code = [
            secrets.choice(ALPHABETS),  # 1st: alphabet
            secrets.choice(NUMBERS),    # 2nd: number
            secrets.choice(NUMBERS),    # 3rd: number
            secrets.choice(ALPHABETS),  # 4th: alphabet
            secrets.choice(ALPHABETS),  # 5th: alphabet
            secrets.choice(NUMBERS),    # 6th: number
        ]

        code = "".join(list_code)

        code_chk = await db.scalar(
            select(Institute).where(
                Institute.institute_code == code
            )
        )

        if code_chk is None:
            return code

# ------ FUNCTION FOR CHECKING IF THE INSTITUTE EXISTS ------
async def chk_institute_exists(
    db: AsyncSession,
    institute_id: int,
) -> Institute | None:
    institute_exists = await db.scalar(
        select(Institute).where(Institute.id == institute_id)
    )

    return institute_exists

