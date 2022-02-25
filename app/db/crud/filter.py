"""All DB functions for the Filter table"""
from typing import Iterable
from typing import List
from typing import Union

import sqlalchemy
from sqlalchemy.orm import Session

from db.base import Allergie
from db.base import Cuisine
from db.base import FilterRest
from db.base import Person
from schemes import scheme_allergie
from schemes import scheme_cuisine
from schemes import scheme_filter
from schemes import scheme_user
from schemes.exceptions import DuplicateEntry
from schemes.exceptions import UserNotFound
from tools.my_logging import logger


def create_filterRest(
    db: Session, filter_new: scheme_filter.FilterRestDatabase, user: scheme_user.UserBase
) -> FilterRest:
    """Create / Add FilterRest to a Person to the Database

    Args:
        db (Session): Session to the DB
        filter (scheme_filter.FilterRestDatabase): Filter to add / create
        user (scheme_user.UserCreate): Person to add the filter

    Raises:
        UserNotFound: Raises if User is missing
        DuplicateEntry: Duplicate Primary Key

    Returns:
        FilterRest: Created Filter
    """

    db_user = db.query(Person).filter(Person.email == user.email).first()
    if not db_user:
        raise UserNotFound(f"User {user.email} not found", user.email)

    db_filter = FilterRest(
        email=db_user.email,
        zipcode=filter_new.zipcode,
        radius=filter_new.radius,
        rating=filter_new.rating,
        costs=filter_new.costs,
        cuisines=__cuisine_scheme_to_model__(db, filter_new.cuisines),
        allergies=__allergies_scheme_to_model__(db, filter_new.allergies),
    )

    try:
        db.add(db_filter)
        db.commit()
        db.refresh(db_filter)

        logger.info("Added FilterRest to db... user:%s", db_user.email)

        return db_filter
    except sqlalchemy.exc.IntegrityError as error:
        raise DuplicateEntry("Filter already exist") from error


def update_filterRest(
    db: Session, updated_filter: scheme_filter.FilterRestDatabase, user: scheme_user.UserBase
) -> FilterRest:
    """Update the Values of a FilterRest

    Args:
        db (Session): Session to the Database
        updated_filter (scheme_filter.FilterRestDatabase): Filter with the new Values. Need also the old Values
        user (scheme_user.UserBase): The User to the Filter

    Raises:
        UserNotFound: Raises if User is missing

    Returns:
        FilterRest: Return the added filter
    """

    db_person: Person = db.query(Person).filter(Person.email == user.email).first()
    if not db_person:
        raise UserNotFound(f"User {user.email} not found", user.email)

    db_person.filterRest.zipcode = updated_filter.zipcode
    db_person.filterRest.radius = str(updated_filter.radius)
    db_person.filterRest.rating = str(updated_filter.rating)
    db_person.filterRest.costs = updated_filter.costs
    db_person.filterRest.cuisines = __cuisine_scheme_to_model__(db, updated_filter.cuisines)
    db_person.filterRest.allergies = __allergies_scheme_to_model__(db, updated_filter.allergies)

    db.commit()
    db.refresh(db_person)

    logger.info("Updated FilterRest from... user:%s", db_person.email)

    return db_person.filterRest


def get_filter_from_user(db: Session, user: scheme_user.UserBase) -> Union[FilterRest, None]:
    """Get the Filter for one User if exists

    Args:
        db (Session): Session to the DB
        user (scheme_user.UserBase): Owner of the Filter

    Returns:
        Union[FilterRest, None]: Return the filter or None
    """
    return db.query(FilterRest).filter(FilterRest.email == user.email).first()


def __allergies_scheme_to_model__(
    db: Session, allergies: List[scheme_allergie.PydanticAllergies]
) -> Union[List[scheme_allergie.PydanticAllergies], scheme_allergie.PydanticAllergies, None]:
    if isinstance(allergies, Iterable):
        return [db.query(Allergie).filter(Allergie.name == allergie.name).first() for allergie in allergies]
    elif allergies is not None:
        return [allergies]
    else:
        return []


def __cuisine_scheme_to_model__(
    db: Session, cuisines: List[scheme_cuisine.PydanticCuisine]
) -> Union[List[scheme_cuisine.PydanticCuisine], scheme_cuisine.PydanticCuisine, None]:
    if isinstance(cuisines, Iterable):
        return [db.query(Cuisine).filter(Cuisine.name == cuisine.name).first() for cuisine in cuisines]
    elif cuisines is not None:
        return [cuisines]
    else:
        return []
