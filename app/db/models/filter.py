"""Filter structure for the DB"""
from db.base import Base
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship


association_table_filter_allergie = Table(
    "association_filter_allergie",
    Base.metadata,
    Column("filterRest_email", ForeignKey("filterRest.email"), primary_key=True),
    Column("allergie_name", ForeignKey("allergie.name"), primary_key=True),
)

association_table_filter_cuisine = Table(
    "association_filter_cuisine",
    Base.metadata,
    Column("filterRest_email", ForeignKey("filterRest.email"), primary_key=True),
    Column("cuisine_name", ForeignKey("cuisine.name"), primary_key=True),
)


class FilterRest(Base):
    """Model for SQLAlchemy for the filter Table in the DB"""

    __tablename__ = "filterRest"

    email = Column(String, ForeignKey("person.email"), primary_key=True)
    zipcode = Column(String(5), nullable=False)
    radius = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    costs = Column(Integer, nullable=False)

    person = relationship("Person", back_populates="filterRest", passive_deletes=True)
    allergies = relationship("Allergie", secondary=association_table_filter_allergie, passive_deletes=True)
    cuisines = relationship("Cuisine", secondary=association_table_filter_cuisine, passive_deletes=True)
