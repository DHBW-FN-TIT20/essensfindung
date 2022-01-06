import fastapi
import uvicorn

from starlette.staticfiles import StaticFiles
from views import home

app = fastapi.FastAPI()


def configure():
    """Init Setup for the application"""
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
