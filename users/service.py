# Importing the User database model
from users.models import User

# Importing the required modules
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# Function to check if user exists or not
async def get_user_by_id(user_id: int, db: AsyncSession) -> User | None:
    """
    Fetches a user from the database by their unique ID.
    Returns the User database model object if found, otherwise returns None.
    """
    statement = select(User).where(user_id == User.id)

    user = await db.scalar(statement)

    return user

