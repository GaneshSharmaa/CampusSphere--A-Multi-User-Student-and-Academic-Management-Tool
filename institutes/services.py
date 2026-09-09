# Importing the required modules
import secrets, string
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

# Importing the database model
from institutes.models import Institute

# Importing the database dependencies
from database.dependencies import get_db

# ------ FUNCTION FOR GENERATING UNIQUE CODES ------
async def generate_code(
    db: Annotated[AsyncSession, Depends(get_db)]
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

        code_chk = await db.execute(
            select(Institute).where(
                Institute.institute_code == code
            )
        )

        if code_chk is None:
            return code
        else:
            continue

