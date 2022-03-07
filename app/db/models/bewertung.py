"""Bewertung structure for the DB"""
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base import Base


class BewertungRestaurant(Base):
    """
    Model for SQLAlchemy for the bewertung Table in the DB

    Attributes:
        person_email (str): Primary Key and ForeignKey of db.models.person.Person email
        place_id (str): Primary Key and ForeignKey of db.models.restaurant.BewertungRestaurant
        zeitstempel (sqlalchemy.DateTime): Set automatic in DB when updated
        kommentar (str): Can be None
        rating (int): Rating if the assessment
        person (db.models.person.Person)
        restaurant (db.models.restaurant.Restaurant)
    """

    __tablename__ = "bewertungRestaurant"

    person_email = Column(String, ForeignKey("person.email", ondelete="CASCADE"), primary_key=True)
    place_id = Column(String, ForeignKey("restaurant.place_id", ondelete="CASCADE"), primary_key=True)
    zeitstempel = Column(DateTime(timezone=True), server_onupdate=func.now(), server_default=func.now())
    kommentar = Column(String, nullable=True)
    rating = Column(Integer, nullable=False)

    person = relationship("Person", back_populates="bewertungenRest")
    restaurant = relationship("Restaurant", back_populates="bewertungen")


class BewertungRecipe(Base):
    """
    Model for SQLAlchemy for the bewertung Table in the DB

    Attributes:
        person_email (str): Primary Key and ForeignKey of db.models.person.Person email
        rezept_id (str): Primary Key and ForeignKey of db.models.restaurant.BewertungRecipe
        rezept_name (str): Can not be None
        zeitstempel (sqlalchemy.DateTime): Set automatic in DB when updated
        kommentar (str): Can be None
        rating (int): Rating if the assessment
        person (db.models.person.Person)
        restaurant (db.models.restaurant.Restaurant)
    """

    __tablename__ = "bewertungRezept"

    person_email = Column(String, ForeignKey("person.email", ondelete="CASCADE"), primary_key=True)
    rezept_id = Column(String, ForeignKey("restaurant.place_id", ondelete="CASCADE"), primary_key=True)
    rezept_name = Column(String, nullable=False)
    zeitstempel = Column(DateTime(timezone=True), server_onupdate=func.now(), server_default=func.now())
    kommentar = Column(String, nullable=True)
    rating = Column(Integer, nullable=False)

    person = relationship("Person", back_populates="bewertungenRezept")
