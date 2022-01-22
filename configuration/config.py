from configparser import ConfigParser
from . import PATH_GOOGLE, PATH_DB


def get_google_api_key() -> str:
    """Get the API-Key for google requests

    Returns:
        str: API-Key
    """
    config = ConfigParser()
    config.read(PATH_GOOGLE)
    key: str = config["API"]["KEY"]
    return key


def get_db_conf() -> dict:
    """Return the importet configuration of the db

    Returns:
        dict: return the values for "username", "password", "host", "database"
    """
    config = ConfigParser()
    config.read(PATH_DB)
    values = {
        "username": config["USER"]["USERNAME"],
        "password": config["USER"]["PASSWORD"],
        "host": config["CONNECTION"]["HOST"],
        "database": config["CONNECTION"]["DATABASE"],
    }
    return values
