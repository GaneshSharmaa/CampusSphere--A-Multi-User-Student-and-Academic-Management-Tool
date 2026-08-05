# importing required modules
import jwt
from jwt import InvalidTokenError
from fastapi import HTTPException, status
from os import getenv
from dotenv import load_dotenv
from datetime import UTC, datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

# load and setting up environment variables
load_dotenv()

# constants
SECRET_KEY = getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MIN = 30
ALGORITHM = "HS256"

# checking if `SECRET_KEY` is empty or not
if SECRET_KEY is None:
    raise ValueError("The secret key is not available.")

# function to create an access token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MIN)

    to_encode["exp"] = expire

    jwt_string = jwt.encode(
        payload = to_encode,
        key = SECRET_KEY,
        algorithm = ALGORITHM
    )

    return jwt_string

# function to verify the access_token
def verify_access_token(token: str) -> str:
    try:
        payload = jwt.decode(
            jwt = token,
            key = SECRET_KEY,
            algorithms = ALGORITHM
        )

        sub = payload.get["sub"]

        if sub is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Could not validate credentials."
            )

        return payload

    except InvalidTokenError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Could not validate credentials."
        )

