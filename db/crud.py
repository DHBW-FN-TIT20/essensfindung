"""CRUD comes from: Create, Read, Update, and Delete... for the Database"""
from typing import List
from schemes import scheme_rest
from sqlalchemy.orm import Session

from . import db_models


def get_restaurant_by_id(db: Session, place_id: str) -> db_models.Restaurant:
    """Search for one Restaurant in the db and return it if found

    Args:
        db (Session): Session to the DB
        place_id (str): ID of the Restaurant to search

    Returns:
        db_models.Restaurant: The found restaurant
    """
    return db.query(db_models.Restaurant).filter(db_models.Restaurant.place_id == place_id).first()


def get_all_restaurants(db: Session, skip: int = 0, limit: int = 100) -> List[db_models.Restaurant]:
    """Return all Restaurants in the DB

    Args:
        db (Session): Session to the DB
        skip (int, optional): Offeset to skip results. Defaults to 0.
        limit (int, optional): Set a Limit to the Result. Defaults to 100.

    Returns:
        List[db_models.Restaurant]: Results
    """
    return db.query(db_models.Restaurant).offset(skip).limit(limit).all()

def create_restaurant(db: Session, rest: scheme_rest.BaseRestaurant) -> db_models.Restaurant:
    """Create / Add a Restaurant to the DB

    Args:
        db (Session): Session to the DB
        rest (scheme_rest.BaseRestaurant): The Restaurant with the place_id required

    Returns:
        db_models.Restaurant: Return if success
    """
    db_rest = db_models.Restaurant(**rest.dict())
    db.add(db_rest)
    db.commit()
    db.refresh(db_rest)
    return db_rest

def delete_restaurant(db: Session, place_id: str) -> int:
    return db.query(db_models.Restaurant).delete(db_models.Restaurant.place_id == place_id)

