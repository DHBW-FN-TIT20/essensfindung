from configparser import ConfigParser

from . import PATH_DB
from . import PATH_GOOGLE

config = ConfigParser()
config.read((PATH_GOOGLE, PATH_DB))


class Setting:
    GOOGLE_API_KEY: str = config["API"]["KEY"]
    POSTGRES_USER: str = config["USER"]["USERNAME"]
    POSTGRES_PASSWORD: str = config["USER"]["PASSWORD"]
    POSTGRES_SERVER: str = config["CONNECTION"]["HOST"]
    POSTGRES_DATABASE: str = config["CONNECTION"]["DATABASE"]


settings = Setting()
