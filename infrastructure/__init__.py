from configparser import ConfigParser
from pathlib import Path
from enum import Enum


class Cuisine(Enum):
    """Docstring for Cuisine."""
    ITALIAN = "Italienisch"
    GERMAN = "Deutsch"
    ASIAN = "Asiatisch"
    DOENER = "Doener"
    TURKEY = "Tuerkisch"


CONF_PATH = Path("./configuration/google_api.conf")


def get_api_key() -> str:
    config = ConfigParser()
    config.read(CONF_PATH)
    key: str = config["API"]["KEY"]
    return key
