"""All DB functions for the Bewertung table"""
from typing import List
from typing import Union

import sqlalchemy
from sqlalchemy.orm import Session

from . import logger
from db.base import Bewertung
from db.base import Person
from db.base import Restaurant
from db.crud.restaurant import get_restaurant_by_id
from db.crud.user import get_user_by_mail
from schemes import scheme_rest
from schemes import scheme_user
from schemes.exceptions import DatabaseException
from schemes.exceptions import DuplicateEntry
from schemes.exceptions import RestaurantNotFound
from schemes.exceptions import UserNotFound


def get_bewertung_from_user_to_rest(
    db: Session, user: scheme_user.UserBase, rest: scheme_rest.RestaurantBase
) -> Bewertung:
    """Return a specific bewertung from a user to only one restaurant

    Args:
        db (Session): Session to the DB
        user (scheme_user.UserBase): Specifie the User
        rest (scheme_rest.RestaurantBase): Specifie the restauranat

    Returns:
        Bewertung: Return one bewertung that match the restaurant - user
    """
    return (
        db.query(Bewertung)
        .join(Person, Person.email == Bewertung.person_email)
        .join(Restaurant, Restaurant.place_id == Bewertung.place_id)
        .filter(Person.email == user.email)
        .filter(Restaurant.place_id == rest.place_id)
        .first()
    )


def get_all_user_bewertungen(db: Session, user: scheme_user.UserBase) -> Union[List[Bewertung], None]:
    """Return all bewertugen from one User

    Args:
        db (Session): Session to the DB
        user (scheme_user.UserBase): The user to select

    Returns:
        List[Bewertung] OR None
    """
    user: Person = get_user_by_mail(db, user.email)
    if user is None:
        return None
    else:
        return user.bewertungen


def create_bewertung(db: Session, assessment: scheme_rest.RestBewertungCreate) -> Bewertung:
    """Create / Add a Bewertung to the DB. Timestamp and ID will set automatic.

    Args:
        db (Session): Session to the DB
        assessment (scheme_rest.RestBewertungCreate): Bewertung to add. This include the Person and Restaurant for the mapping of the Bewertung

    Raises:
        UserNotFound: If the user does not exist
        RestaurantNotFound: If the restaurant does not exist
        DuplicateEntry: Duplicate Primary Key

    Returns:
        Bewertung: Return if success
    """
    if get_user_by_mail(db, assessment.person.email) is None:
        raise UserNotFound(f"User {assessment.person.email} does not exist", assessment.person.email)
    if get_restaurant_by_id(db, assessment.restaurant.place_id) is None:
        raise RestaurantNotFound("Restaurant does not exist", assessment.restaurant.place_id)

    db_assessment = Bewertung(
        person_email=assessment.person.email,
        place_id=assessment.restaurant.place_id,
        kommentar=assessment.comment,
        rating=assessment.rating,
    )
    try:
        db.add(db_assessment)
        db.commit()
        db.refresh(db_assessment)
        logger.info(
            "Added assessment to db... place_id:%s\temail%s\trating:%s\tcomment:%s",
            db_assessment.place_id,
            db_assessment.person_email,
            db_assessment.rating,
            db_assessment.kommentar,
        )
        return db_assessment
    except sqlalchemy.exc.IntegrityError as error:
        raise DuplicateEntry("Assessment already exist") from error


def update_bewertung(
    db: Session, old_bewertung: scheme_rest.RestBewertungCreate, new_bewertung: scheme_rest.RestBewertungCreate
) -> Bewertung:
    """Update the comment and rating of a bewertung

    Args:
        db (Session): Session to the DB
        old_bewertung (scheme_rest.RestBewertungCreate): The old Bewertung
        new_bewertung (scheme_rest.RestBewertungCreate): The updated Bewertung

    Returns:
        Bewertung: New Bewertung from `get_bewertung_from_user_to_rest`
    """
    rows = (
        db.query(Bewertung)
        .filter(Bewertung.person_email == old_bewertung.person.email)
        .filter(Bewertung.place_id == old_bewertung.restaurant.place_id)
        .update({Bewertung.kommentar: new_bewertung.comment, Bewertung.rating: new_bewertung.rating})
    )

    if rows == 0:
        raise DatabaseException("Can not update assessment. Does the User and the Restaurant exist?")

    db.commit()
    logger.info("Updated bewertung %s - %s", old_bewertung.person.email, old_bewertung.restaurant.place_id)
    return get_bewertung_from_user_to_rest(db, new_bewertung.person, new_bewertung.restaurant)


def delete_bewertung(db: Session, user: scheme_user.UserBase, rest: scheme_rest.RestaurantBase) -> int:
    """Delete one Bewertung

    Args:
        db (Session): Session to the db
        user (scheme_user.User): The owner of the Bewertung
        rest (scheme_rest.RestaurantBase): The corrosponding Restaurant

    Returns:
        int: Number of effected rows
    """
    rows = (
        db.query(Bewertung).filter(Bewertung.person_email == user.email, Bewertung.place_id == rest.place_id).delete()
    )
    db.commit()
    logger.info("Deleted bewertung %s - %s", user.email, rest.place_id)
    return rows
