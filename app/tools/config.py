"""Here you can setup and find all needed configurations"""
import os
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path("./.env")
load_dotenv(dotenv_path=ENV_PATH)


class Setting:
    """
    Contains all Settings - Loads from the os env

    Warning:
        Do not create your own instance! Import settings instead from this module!

    Note:
        Do not modifie SQL_LITE by yourself

    Attributes:
        GOOGLE_API_KEY (str): Google API Key
        SECRET_KEY (str): Key that is used for the JWT hashing
        ALGORITHM (str): Used hash algorit. Defaults to HS256
        ACCESS_TOKEN_EXPIRE_MINUTES (int): How long JWT - Token is valid in Minutes. Defaults to 30
        SQL_LITE (bool): Automatic set to True if POSTGRES_SERVER is set
        POSTGRES_USER (str): User for the DB
        POSTGRES_PASSWORD (str): Password for the user
        POSTGRES_SERVER (str): FQDN or IP of the DB Server
        POSTGRES_DATABASE (str): Name of the Database
        POSTGRES_PORT (str): Port of the Server
    """

    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    if os.getenv("POSTGRES_SERVER"):
        SQL_LITE: bool = False
        POSTGRES_USER: str = os.getenv("POSTGRES_USER")
        POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
        POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
        POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE")
        POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    else:
        SQL_LITE: bool = True


settings = Setting()
"""Import this to gain the initial settings"""
