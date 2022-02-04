"""Person structure for the DB"""
from db.base import Base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Person(Base):
    """Model for SQLAlchemy for the person Table in the DB"""

    __tablename__ = "person"

    email = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)
    last_login = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    bewertungen = relationship("Bewertung", back_populates="person", passive_deletes=True)
    filter = relationship("Filter", back_populates="person", passive_deletes=True)
