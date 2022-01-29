"""Create the Base Model for all Tabels in the Database"""
from typing import Any

from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id: Any
    __name__: str
