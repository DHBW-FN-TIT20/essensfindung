"""Main entry Point for the Application"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from db import db_models
from db.database import engine
from views import restaurant
from views import index, restaurant

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
    file_h.setLevel(logging.ERROR)

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


def configure_database():
    """Configure connection to the Database"""
    db_models.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    configure()
    uvicorn.run(app, port=8000, host="192.168.178.44")
else:
    configure()
