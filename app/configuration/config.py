import os
from pathlib import Path

from dotenv import load_dotenv

ENV_PATH = Path("./configuration/.env")
load_dotenv(dotenv_path=ENV_PATH)


class Setting:
    """Contains all Settings - Loads from the os env"""

    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")


settings = Setting()
