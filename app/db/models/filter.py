"""Filter structure for the DB"""
from db.base import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship


association_table_filter_allergie = Table(
    "association",
    Base.metadata,
    Column("filterRest_email", ForeignKey("filterRest.email"), primary_key=True),
    Column("allergie_name", ForeignKey("allergie.name"), primary_key=True),
)


class FilterRest(Base):
    """Model for SQLAlchemy for the filter Table in the DB"""

    __tablename__ = "filterRest"

    email = Column(String, ForeignKey("person.email"), primary_key=True)
    plz = Column(String(5), nullable=False)
    radius = Column(Integer, nullable=False)
    g_rating = Column(Integer, nullable=False)
    cuisine = Column(String, nullable=False)

    person = relationship("Person", back_populates="filterRest", passive_deletes=True)
    allergies = relationship("Allergie", secondary=association_table_filter_allergie, passive_deletes=True)
