"""Allergie structure for the DB"""
from db.base import Base
from sqlalchemy import Column
from sqlalchemy import String


class Allergie(Base):
    """Model for SQLAlchemy for the allergie Table in the DB"""

    __tablename__ = "allergie"

    name = Column(String, primary_key=True)
    beschreibung = Column(String)
