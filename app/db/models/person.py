"""Person structure for the DB"""
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base import Base


class Person(Base):
    """Model for SQLAlchemy for the person Table in the DB"""

    __tablename__ = "person"

    email = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)
    last_login = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    bewertungen = relationship("Bewertung", back_populates="person", passive_deletes=True)
    filterRest = relationship("FilterRest", back_populates="person", uselist=False, passive_deletes=True)
