"""SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database"""
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.database import Base

association_table_filter_allergie = Table(
    "association",
    Base.metadata,
    Column("filter_email", ForeignKey("filter.email")),
    Column("allergie_name", ForeignKey("allergie.name")),
)


class Person(Base):
    """Model for SQLAlchemy for the person Table in the DB"""

    __tablename__ = "person"

    email = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)
    last_login = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    bewertungen = relationship("Bewertung", back_populates="person", passive_deletes=True)
    filter = relationship("Filter", back_populates="person", passive_deletes=True)


class Restaurant(Base):
    """Model for SQLAlchemy for the restaurant Table in the DB"""

    __tablename__ = "restaurant"

    place_id = Column(String, primary_key=True)

    bewertungen = relationship("Bewertung", back_populates="restaurant", passive_deletes=True)


class Bewertung(Base):
    """Model for SQLAlchemy for the bewertung Table in the DB"""

    __tablename__ = "bewertung"

    person_email = Column(String, ForeignKey("person.email", ondelete="CASCADE"), primary_key=True)
    place_id = Column(String, ForeignKey("restaurant.place_id", ondelete="CASCADE"), primary_key=True)
    zeitstempel = Column(DateTime(timezone=True), server_onupdate=func.now(), server_default=func.now())
    kommentar = Column(String, nullable=True)
    rating = Column(Integer, nullable=False)

    person = relationship("Person", back_populates="bewertungen")
    restaurant = relationship("Restaurant", back_populates="bewertungen")


class Filter(Base):
    """Model for SQLAlchemy for the filter Table in the DB"""

    __tablename__ = "filter"

    email = Column(String, ForeignKey("person.email"), primary_key=True)
    plz = Column(String(5), nullable=False)
    radius = Column(Integer, nullable=False)
    g_rating = Column(Integer, nullable=False)
    cuisine = Column(String, nullable=False)

    person = relationship("Person", back_populates="filter")
    allergien = relationship("Allergie", secondary=association_table_filter_allergie)


class Allergie(Base):
    """Model for SQLAlchemy for the allergie Table in the DB"""

    __tablename__ = "allergie"

    name = Column(String, primary_key=True)
    beschreibung = Column(String)
