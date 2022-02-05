"""All DB functions for the User table"""
from typing import Iterable
from typing import List
from typing import Union

import sqlalchemy
from sqlalchemy.orm import Session

from db.base import Allergie
from db.base import FilterRest
from db.base import Person
from schemes import scheme_filter
from schemes import scheme_user


def create_filterRest(
    db: Session, filter_new: scheme_filter.FilterRestDatabase, user: scheme_user.UserBase
) -> FilterRest:
    """Create / Add FilterRest to a Person to the Database

    Args:
        db (Session): Session to the DB
        filter (scheme_filter.FilterRestDatabase): Filter to add / create
        user (scheme_user.UserCreate): Person to add the filter

    Raises:
        sqlalchemy.exc.NoForeignKeysError: Raises if User is missing

    Returns:
        FilterRest: Created Filter
    """

    db_user = db.query(Person).filter(Person.email == user.email).first()
    if not db_user:
        raise sqlalchemy.exc.NoForeignKeysError("Missing User")

    db_filter = FilterRest(
        email=db_user.email,
        zipcode=filter_new.zipcode,
        radius=filter_new.radius,
        rating=filter_new.rating,
        cuisine=filter_new.cuisine.value,
        costs=filter_new.costs,
        allergies=__allergies_scheme_to_model__(db, filter_new.allergies),
    )

    db.add(db_filter)
    db.commit()
    db.refresh(db_filter)

    return db_filter


def update_filterRest(
    db: Session, updated_filter: scheme_filter.FilterRestDatabase, user: scheme_user.UserBase
) -> FilterRest:
    """Update the Values of a FilterRest

    Args:
        db (Session): Session to the Database
        updated_filter (scheme_filter.FilterRestDatabase): Filter with the new Values. Need also the old Values
        user (scheme_user.UserBase): The User to the Filter

    Returns:
        FilterRest: Return the added filter
    """

    db_person: Person = db.query(Person).filter(Person.email == user.email).first()

    db_person.filterRest.zipcode = updated_filter.zipcode
    db_person.filterRest.radius = str(updated_filter.radius)
    db_person.filterRest.rating = str(updated_filter.rating)
    db_person.filterRest.cuisine = updated_filter.cuisine.value
    db_person.filterRest.costs = updated_filter.costs
    db_person.filterRest.allergies = __allergies_scheme_to_model__(db, updated_filter.allergies)

    db.commit()
    db.refresh(db_person)
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
    db: Session, allergies: List[scheme_filter.FilterRestDatabase]
) -> Union[List[FilterRest], FilterRest, None]:
    if isinstance(allergies, Iterable):
        return [db.query(Allergie).filter(Allergie.name == allergie.name).first() for allergie in allergies]
    elif allergies is not None:
        return [allergies]
    else:
        return []
