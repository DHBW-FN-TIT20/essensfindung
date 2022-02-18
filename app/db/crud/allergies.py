from typing import List

import sqlalchemy
from sqlalchemy.orm import Session

import schemes
from db.base import Allergie
from schemes.exceptions import DuplicateEntry
from tools.my_logging import logger


def create_allergie(db: Session, allergie: schemes.Allergies) -> Allergie:
    """Add a single allergie to the DB to select later

    Args:
        db (Session): Session to the db
        allergie (scheme_allergie.Allergie): Allergie to be added

    Raises:
        DuplicateEntry: Duplicate Primary Key

    Returns:
        Allergie: return the db Allergie if success
    """
    try:
        db_allergie = Allergie(name=allergie.value)
        db.add(db_allergie)
        db.commit()
        db.refresh(db_allergie)

        logger.info("Added allergie to db... name:%s", db_allergie.name)

        return db_allergie
    except sqlalchemy.exc.IntegrityError as error:
        raise DuplicateEntry(f"Allergie {allergie.value} already exist in the Database") from error


def get_all_allergies(db: Session) -> List[Allergie]:
    """Get all Allergies in the DB

    Args:
        db (Session): Session to the DB

    Returns:
        List[Allergie]: List of Allergies
    """
    return db.query(Allergie).all()
