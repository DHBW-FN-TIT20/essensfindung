import logging
from pathlib import Path

import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles

from views import home

app = fastapi.FastAPI()
LOGGING_PATH = Path("./logs/infos.log")


def configure():
    """Init Setup for the application"""
    logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", filename=LOGGING_PATH, level=logging.DEBUG)

    configure_routing()
    configure_database()


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
