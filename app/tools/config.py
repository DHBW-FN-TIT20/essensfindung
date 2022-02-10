import os
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path("./.env")
load_dotenv(dotenv_path=ENV_PATH)


class Setting:
    """Contains all Settings - Loads from the os env"""

    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

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
