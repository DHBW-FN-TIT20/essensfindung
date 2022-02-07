from typing import List

from sqlalchemy.orm import Session

import schemes
from . import logger
from db.base import Allergie


def create_allergie(db: Session, allergie: schemes.Allergies) -> Allergie:
    """Add a single allergie to the DB to select later

    Args:
        db (Session): Session to the db
        allergie (scheme_allergie.Allergie): Allergie to be added

    Returns:
        Allergie: return the db Allergie if success
    """
    db_allergie = Allergie(name=allergie.value)
    db.add(db_allergie)
    db.commit()
    db.refresh(db_allergie)

    logger.info("Added allergie to db... name:%s", db_allergie.name)

    return db_allergie


def get_all_allergies(db: Session) -> List[Allergie]:
    """Get all Allergies in the DB

    Args:
        db (Session): Session to the DB

    Returns:
        List[Allergie]: List of Allergies
    """
    return db.query(Allergie).all()
