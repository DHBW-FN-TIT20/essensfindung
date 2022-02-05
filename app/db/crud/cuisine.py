from typing import List

from sqlalchemy.orm import Session

import schemes
from db.base import Cuisine


def create_cuisine(db: Session, cuisine: schemes.Cuisine) -> Cuisine:
    """Add a single cuisine to the DB to select later

    Args:
        db (Session): Session to the db
        cuisine (scheme_allergie.Cuisine): Cuisine to be added

    Returns:
        Cuisine: return the db Cuisine if success
    """
    db_cuisine = Cuisine(name=cuisine.value)
    db.add(db_cuisine)
    db.commit()
    db.refresh(db_cuisine)
    return db_cuisine


def get_all_allergies(db: Session) -> List[Cuisine]:
    """Get all Allergies in the DB

    Args:
        db (Session): Session to the DB

    Returns:
        List[Cuisine]: List of Allergies
    """
    return db.query(Cuisine).all()
