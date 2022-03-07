"""Person structure for the DB"""
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base import Base


class Person(Base):
    """
    Model for SQLAlchemy for the person Table in the DB

    Attributes:
        email (str): Primary Key
        hashed_password (str): Hashed Password of the user
        last_login (sqlalchemy.DateTime): Autamtic set on update
        bewertungen (db.models.bewertung.BewertungRestaurant): Bewertungen of the Person
        filterRest (db.models.filter.Filter): Saved Filter of the Person

    """

    __tablename__ = "person"

    email = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)
    last_login = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    bewertungenRest = relationship("BewertungRestaurant", back_populates="person", passive_deletes=True)
    bewertungenRezept = relationship("BewertungRecipe", back_populates="person", passive_deletes=True)
    filterRest = relationship("FilterRest", back_populates="person", uselist=False, passive_deletes=True)
