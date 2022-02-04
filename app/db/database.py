"""Create the connection to the Database"""
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tools.config import settings

if settings.SQL_LITE:
    Path("./data").mkdir(exist_ok=True)
    SQLALCHEMY_DATABASE_URL = "sqlite:///./data/essensfindung.db"
    # Use connect_args parameter only with sqlite
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DATABASE}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        database = SessionLocal()
        yield database
    finally:
        database.close()
