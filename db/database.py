"""Create the connection to the Database"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configuration import config

conf = config.get_db_conf()
SQLALCHEMY_DATABASE_URL = f"postgresql://{conf['username']}:{conf['password']}@{conf['host']}/{conf['database']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        database = SessionLocal()
        yield database
    finally:
        database.close()
