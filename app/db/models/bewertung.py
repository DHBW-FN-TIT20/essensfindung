"""Bewertung structure for the DB"""
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base import Base


class Bewertung(Base):
    """
    Model for SQLAlchemy for the bewertung Table in the DB

    Attributes:
        person_email (str): Primary Key and ForeignKey of db.models.person.Person email
        place_id (str): Primary Key and ForeignKey of db.models.restaurant.Restaurant
        zeitstempel (sqlalchemy.DateTime): Set automatic in DB when updated
        kommentar (str): Can be None
        rating (int): Rating if the assessment
        person (db.models.person.Person)
        restaurant (db.models.restaurant.Restaurant)
    """

    __tablename__ = "bewertung"

    person_email = Column(String, ForeignKey("person.email", ondelete="CASCADE"), primary_key=True)
    place_id = Column(String, ForeignKey("restaurant.place_id", ondelete="CASCADE"), primary_key=True)
    zeitstempel = Column(DateTime(timezone=True), server_onupdate=func.now(), server_default=func.now())
    kommentar = Column(String, nullable=True)
    rating = Column(Integer, nullable=False)

    person = relationship("Person", back_populates="bewertungen")
    restaurant = relationship("Restaurant", back_populates="bewertungen")
