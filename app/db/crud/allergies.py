from typing import List

import schemes
from db.base import Allergie
from sqlalchemy.orm import Session


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
    return db_allergie


def get_all_allergies(db: Session) -> List[Allergie]:
    """Get all Allergies in the DB

    Args:
        db (Session): Session to the DB

    Returns:
        List[Allergie]: List of Allergies
    """
    return db.query(Allergie).all()
