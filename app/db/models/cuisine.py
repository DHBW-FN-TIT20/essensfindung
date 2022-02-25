"""Filter structure for the DB"""
from sqlalchemy import Column
from sqlalchemy import String

from db.base import Base


class Cuisine(Base):
    """
    Model for SQLAlchemy for the Cuisine Table in the DB

    Attributes:
        name (str): Primary Key
    """

    __tablename__ = "cuisine"

    name = Column(String, primary_key=True)
