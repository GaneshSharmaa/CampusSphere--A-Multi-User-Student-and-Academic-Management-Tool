from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set.")

engine = create_async_engine(
    DATABASE_URL,
    echo = False,
    pool_pre_ping = True
)

SessionLocal = async_sessionmaker(
    bind = engine,
    expire_on_commit = False,
    autoflush = False
)

class Base(DeclarativeBase):
    pass

