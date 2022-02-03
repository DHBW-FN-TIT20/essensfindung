"""Basic tools and definitions for the infrastracture"""
from configparser import ConfigParser
from pathlib import Path


def get_api_key() -> str:
    """Get the API-Key for google requests

    Returns:
        str: API-Key
    """
    conf_path = Path("./configuration/google_api.conf")
    config = ConfigParser()
    config.read(conf_path)
    key: str = config["API"]["KEY"]
    return key
