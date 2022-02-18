"""All DB functions for the Restaurant table"""
from typing import List

import sqlalchemy
from sqlalchemy.orm import Session

from db.base import Restaurant
from schemes import scheme_rest
from schemes.exceptions import DuplicateEntry
from tools.my_logging import logger


def get_restaurant_by_id(db: Session, place_id: str) -> Restaurant:
    """Search for one Restaurant in the db and return it if found

    Args:
        db (Session): Session to the DB
        place_id (str): ID of the Restaurant to search

    Returns:
        Restaurant: The found restaurant
    """
    return db.query(Restaurant).filter(Restaurant.place_id == place_id).first()


def get_all_restaurants(db: Session, skip: int = 0, limit: int = 100) -> List[Restaurant]:
    """Return all Restaurants in the DB

    Args:
        db (Session): Session to the DB
        skip (int, optional): Offeset to skip results. Defaults to 0.
        limit (int, optional): Set a Limit to the Result. Defaults to 100.

    Returns:
        List[Restaurant]: Results
    """
    return db.query(Restaurant).offset(skip).limit(limit).all()


def create_restaurant(db: Session, rest: scheme_rest.RestaurantCreate) -> Restaurant:
    """Create / Add a Restaurant to the DB

    Args:
        db (Session): Session to the DB
        rest (scheme_rest.RestaurantBase): The Restaurant with the place_id required

    Raises:
        DuplicateEntry: Duplicate Primary Key

    Returns:
        Restaurant: Return if success
    """
    try:
        db_rest = Restaurant(place_id=rest.place_id, name=rest.name)
        db.add(db_rest)
        db.commit()
        db.refresh(db_rest)

        logger.info("Added Restaurant to db... place_id:%s", db_rest.place_id)

        return db_rest
    except sqlalchemy.exc.IntegrityError as error:
        raise DuplicateEntry(f"Restaurant {rest.place_id} already in the Database") from error


def delete_restaurant(db: Session, rest: scheme_rest.RestaurantBase) -> int:
    """Delete one restaurant from the DB with the specific place_id

    Args:
        db (Session): Session to the DB
        rest (RestaurantBase): Restaurant with the place_id

    Returns:
        int: Number of effected rows
    """
    rows = db.query(Restaurant).filter(Restaurant.place_id == rest.place_id).delete()
    db.commit()

    logger.info("Removed Restaurant from db... place_id:%s", rest.place_id)

    return rows
