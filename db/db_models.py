"""SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database"""
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from db.database import Base


class Person(Base):
    """Model for SQLAlchemy for the person Table in the DB"""

    __tablename__ = "person"

    email = Column(String, primary_key=True)
    hashed_password = Column(String)
    last_login = Column(DateTime(timezone=True), server_default=func.now())


class BewPers(Base):
    """Model for SQLAlchemy for the bewPers Table in the DB"""

    __tablename__ = "bewPers"
    bewertung_id = Column(Integer, ForeignKey("bewertung.id"), primary_key=True)
    email = Column(String, ForeignKey("person.email"), primary_key=True)


class Restaurant(Base):
    """Model for SQLAlchemy for the restaurant Table in the DB"""

    __tablename__ = "restaurant"

    place_id = Column(String, primary_key=True)


class BewRest(Base):
    """Model for SQLAlchemy for the bewRest Table in the DB"""

    __tablename__ = "bewRest"

    bewertung_id = Column(Integer, ForeignKey("bewertung.id"), primary_key=True)
    place_id = Column(String, ForeignKey("restaurant.place_id"), primary_key=True)


class Bewertung(Base):
    """Model for SQLAlchemy for the bewertung Table in the DB"""

    __tablename__ = "bewertung"

    id = Column(Integer, primary_key=True, autoincrement=True)
    zeitstempel = Column(DateTime(timezone=True), server_onupdate=func.now(), server_default=func.now())
    kommentar = Column(String)
    rating = Column(Integer, autoincrement=False)


class Filter(Base):
    """Model for SQLAlchemy for the filter Table in the DB"""

    __tablename__ = "filter"

    email = Column(String, ForeignKey("person.email"), primary_key=True)
    plz = Column(String(5))
    radius = Column(Integer)
    g_rating = Column(Integer)
    cuisine = Column(String)
    allergie = Column(Integer, unique=True)


class Allergie(Base):
    """Model for SQLAlchemy for the allergie Table in the DB"""

    __tablename__ = "allergie"

    name = Column(String, primary_key=True)
    beschreibung = Column(String)


class FilterAllergien(Base):
    """Model for SQLAlchemy for the filterAllergien Table in the DB"""

    __tablename__ = "filterAllergien"

    allergie = Column(Integer, ForeignKey("filter.allergie"), primary_key=True)
    name = Column(String, ForeignKey("allergie.name"), primary_key=True)
