"""Create the connection to the Database"""
from typing import Generator

from configuration import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

conf = config.get_db_conf()
SQLALCHEMY_DATABASE_URL = f"postgresql://{conf['username']}:{conf['password']}@{conf['host']}/{conf['database']}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    try:
        database = SessionLocal()
        yield database
    finally:
        database.close()
