"""Filter structure for the DB"""
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from db.base import Base


association_table_filter_allergie = Table(
    "association",
    Base.metadata,
    Column("filter_email", ForeignKey("filter.email")),
    Column("allergie_name", ForeignKey("allergie.name")),
)


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
