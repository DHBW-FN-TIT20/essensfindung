import os
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path("./.env")
load_dotenv(dotenv_path=ENV_PATH)


class Setting:
    """Contains all Settings - Loads from the os env"""

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
