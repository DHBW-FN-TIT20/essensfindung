"""All DB functions for the User table"""
from typing import Iterable
from typing import List
from typing import Union

import sqlalchemy
from db.base import Allergie
from db.base import FilterRest
from db.base import Person
from schemes import scheme_filter
from schemes import scheme_user
from sqlalchemy.orm import Session


def create_filterRest(
    db: Session, filter_new: scheme_filter.FilterRestDatabase, user: scheme_user.UserBase
) -> FilterRest:
    """Create / Add FilterRest to a Person to the Database

    Args:
        db (Session): Session to the DB
        filter (scheme_filter.FilterRestDatabase): Filter to add / create
        user (scheme_user.UserCreate): Person to add the filter

    Returns:
        FilterRest: Created Filter
    """

    db_user = db.query(Person).filter(Person.email == user.email).first()
    if not db_user:
        raise sqlalchemy.exc.NoForeignKeysError("Missing User")

    db_filter = FilterRest(
        email=db_user.email,
        plz=filter_new.zipcode,
        radius=filter_new.radius,
        g_rating=filter_new.rating,
        cuisine=filter_new.cuisine.value,
    )

    db_filter.allergies = __allergies_scheme_to_model__(db, filter_new.allergies)

    db.add(db_filter)
    db.commit()
    db.refresh(db_filter)

    return db_filter


def update_filterRest(
    db: Session, updated_filter: scheme_filter.FilterRestDatabase, user: scheme_user.UserBase
) -> FilterRest:

    db_person: Person = db.query(Person).filter(Person.email == user.email).first()

    # db_current_filter: FilterRest = db_person.filterRest
    db_person.filterRest.plz = updated_filter.zipcode
    db_person.filterRest.radius = str(updated_filter.radius)
    db_person.filterRest.g_rating = str(updated_filter.rating)
    db_person.filterRest.cuisine = updated_filter.cuisine.value
    db_person.filterRest.allergies = __allergies_scheme_to_model__(db, updated_filter.allergies)

    db.commit()
    db.refresh(db_person)
    return db_person.filterRest

    # db_updated_filter = FilterRest(
    #     email=user.email,
    #     plz=updated_filter.zipcode,
    #     radius=updated_filter.radius,
    #     g_rating=updated_filter.rating,
    #     cuisine=updated_filter.cuisine.value,
    # )
    # db_updated_filter.allergies = __allergies_scheme_to_model__(db, updated_filter.allergies)

    # db_person.filterRest = db_updated_filter
    # db.commit()
    # db.refresh(db_updated_filter)

    # return db_updated_filter


def __allergies_scheme_to_model__(
    db: Session, allergies: List[scheme_filter.FilterRestDatabase]
) -> Union[List[FilterRest], FilterRest, None]:
    if isinstance(allergies, Iterable):
        return [db.query(Allergie).filter(Allergie.name == allergie.value).first() for allergie in allergies]
    elif allergies is not None:
        return [allergies]
    else:
        return []
