"""Main entry Point for the Application"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import fastapi
import uvicorn
from sqlalchemy import exc
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from db.base import Base
from db.crud.allergies import create_allergie
from db.crud.cuisine import create_cuisine
from db.database import engine
from schemes import Allergies
from schemes import Cuisine
from views import index
from views import restaurant
from views import signin

app = fastapi.FastAPI()


def configure():
    """Init Setup for the application"""
    configure_logger()
    configure_routing()
    configure_database()


def configure_logger():
    """Configure root logger"""
    # create directory and file if not exist
    logging_path = Path("./logs/infos.log")
    logging_path.parent.mkdir(exist_ok=True)
    logging_path.touch(exist_ok=True)

    # start Configuration
    logger = logging.getLogger()

    # create handler
    stream_h = logging.StreamHandler()
    file_h = logging.FileHandler(logging_path)
    backup_h = RotatingFileHandler(logging_path, maxBytes=10000, backupCount=5)

    # level and formatter
    stream_h.setLevel(logging.WARNING)
    file_h.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
    stream_h.setFormatter(formatter)
    file_h.setFormatter(formatter)

    # add handler
    logger.addHandler(stream_h)
    logger.addHandler(file_h)
    logger.addHandler(backup_h)


def configure_routing():
    """Add / Configure all router for FastAPI"""
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(index.router)
    app.include_router(restaurant.router)
    app.include_router(signin.router)


def configure_database():
    """Configure connection to the Database"""
    try:
        create_database_table()
        add_all_allergies()
    except (exc.OperationalError, exc.IntegrityError):
        # Ignore if Tables already configured
        pass


def create_database_table():
    """Create the Table of the DB"""
    Base.metadata.create_all(bind=engine)


def add_all_allergies():
    """Add all Allergies from the Enum to the DB"""
    with Session(engine) as session:
        for allergie in Allergies:
            create_allergie(session, allergie)


def add_all_cuisine():
    """Add all Allergies from the Enum to the DB"""
    with Session(engine) as session:
        for cuisine in Cuisine:
            create_cuisine(session, cuisine)


if __name__ == "__main__":
    configure()
    uvicorn.run(app, port=8000, host="127.0.0.1")
else:
    configure()
