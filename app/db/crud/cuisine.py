from typing import List

import sqlalchemy
from sqlalchemy.orm import Session

import schemes
from . import logger
from db.base import Cuisine
from schemes.exceptions import DuplicateEntry


def create_cuisine(db: Session, cuisine: schemes.Cuisine) -> Cuisine:
    """Add a single cuisine to the DB to select later

    Args:
        db (Session): Session to the db
        cuisine (scheme_allergie.Cuisine): Cuisine to be added

    Raises:
        DuplicateEntry: Duplicate Primary Key

    Returns:
        Cuisine: return the db Cuisine if success
    """
    try:
        db_cuisine = Cuisine(name=cuisine.value)
        db.add(db_cuisine)
        db.commit()
        db.refresh(db_cuisine)
        logger.info("Added cuisine to db... name:%s", db_cuisine.name)
        return db_cuisine
    except sqlalchemy.exc.IntegrityError as error:
        raise DuplicateEntry(f"Cuisine {cuisine.value} already exist") from error


def get_all_allergies(db: Session) -> List[Cuisine]:
    """Get all Allergies in the DB

    Args:
        db (Session): Session to the DB

    Returns:
        List[Cuisine]: List of Allergies
    """
    return db.query(Cuisine).all()
