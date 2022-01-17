import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from views import home

app = fastapi.FastAPI()


def configure():
    """Init Setup for the application"""
    configure_logger()
    configure_routing()
    configure_database()


def configure_logger():
    """Configure root logger"""
    logging_path = Path("./logs/infos.log")
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


def configure_routing():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(home.router)


def configure_database():
    pass


if __name__ == "__main__":
    configure()
    uvicorn.run(app, port=8000, host="127.0.0.1")
else:
    configure()
