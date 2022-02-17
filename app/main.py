"""Main entry Point for the Application"""
import fastapi
import uvicorn
from fastapi import status
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from db.base import Base
from db.crud.allergies import create_allergie
from db.crud.cuisine import create_cuisine
from db.database import engine
from schemes import Allergies
from schemes import Cuisine
from schemes import exceptions
from schemes.exceptions import DuplicateEntry
from tools.my_logging import logger
from tools.my_logging import setup_logging
from views import error
from views import index
from views import rating
from views import restaurant
from views import signin


app = fastapi.FastAPI(title="Essensfindung")


def configure():
    """Init Setup for the application"""
    setup_logging()
    configure_routing()
    configure_database()


def configure_routing():
    """Add / Configure all router for FastAPI"""
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(index.router)
    app.include_router(restaurant.router)
    app.include_router(signin.router)
    app.include_router(error.router)
    app.include_router(rating.router)


def configure_database():
    """Configure connection to the Database"""
    create_database_table()
    add_all_allergies()
    add_all_cuisine()


def create_database_table():
    """Create the Table of the DB"""
    Base.metadata.create_all(bind=engine, checkfirst=True)


def add_all_allergies():
    """Add all Allergies from the Enum to the DB"""
    for allergie in Allergies:
        with Session(engine) as session:
            try:
                create_allergie(session, allergie)
            except DuplicateEntry:
                pass


def add_all_cuisine():
    """Add all Allergies from the Enum to the DB"""
    for cuisine in Cuisine:
        with Session(engine) as session:
            try:
                create_cuisine(session, cuisine)
            except DuplicateEntry:
                pass


@app.exception_handler(exceptions.DatabaseException)
async def database_exception_handler(request: fastapi.Request, exc: exceptions.DatabaseException):
    """Exception Handler for all DatabaseExceptions made and unhandeld

    Args:
        request: Request for the api
        exc (ServiceError): Raised Exception

    Returns:
        fastapi.responses.RedirectResponse: Redirect to the error page
    """
    logger.exception("Database Error on %s", request.url)
    return fastapi.responses.RedirectResponse(url=f"/error?err_msg={str(exc)}")


@app.exception_handler(exceptions.NoResultsException)
async def search_exception_handler(request: fastapi.Request, exc: exceptions.NoResultsException):
    """Exception Handler for all search Exceptions made and unhandeld

    Args:
        request: Request for the api
        exc (ServiceError): Raised Exception

    Returns:
        fastapi.responses.RedirectResponse: Redirect to the error page
    """
    logger.info("%s URL: %s", str(exc), request.url)
    return fastapi.responses.RedirectResponse(url=f"/error?err_msg={str(exc)}")


@app.exception_handler(exceptions.NotAuthorizedException)
async def authentication_exception_handler(request: fastapi.Request, exc: exceptions.NotAuthorizedException):
    """Exception Handler for accessing a page with wrong ore None credentials

    Args:
        request (fastapi.Request): Request for the url
        exc (exceptions.NotAuthorizedException): Raised Exception

    Returns:
        fastapi.responses.RedirectResponse: Redirect to the siging page
    """
    logger.warning("%s on %s", exc.error_msg, request.url)
    url = str(request.url).replace("&", "%26")
    return fastapi.responses.RedirectResponse(url=f"/signin/?url={url}", headers=exc.headers)


@app.exception_handler(Exception)
async def general_exception_handler(request: fastapi.Request, exc: Exception):
    """Exception Handler for all Exceptions made and unhandeld

    Args:
        request: Request for the api
        exc (ServiceError): Raised Exception

    Returns:
        fastapi.responses.RedirectResponse: Redirect to the error page
    """
    logger.exception("Internal Server Error on %s", request.url)
    return fastapi.responses.RedirectResponse(url=f"/error?err_msg={str(exc)}", status_code=status.HTTP_302_FOUND)


if __name__ == "__main__":
    configure()
    uvicorn.run(app, port=8000, host="192.168.0.112")
else:
    configure()
