"""CRUD comes from: Create, Read, Update, and Delete... for the Database"""
from typing import List, Union

import sqlalchemy

from schemes import scheme_rest, scheme_user
from sqlalchemy.orm import Session
from tools.hashing import Hasher

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


def delete_restaurant(db: Session, rest: scheme_rest.BaseRestaurant) -> int:
    """Delete one restaurant from the DB with the specific place_id

    Args:
        db (Session): Session to the DB
        rest (BaseRestaurant): Restaurant with the place_id

    Returns:
        int: Number of effected rows
    """
    rows = db.query(db_models.Restaurant).filter(db_models.Restaurant.place_id == rest.place_id).delete()
    db.commit()
    return rows


def get_bewertung_from_user_to_rest(
    db: Session, user: scheme_user.UserBase, rest: scheme_rest.BaseRestaurant
) -> db_models.Bewertung:
    """Return a specific bewertung from a user to only one restaurant

    Args:
        db (Session): Session to the DB
        user (scheme_user.UserBase): Specifie the User
        rest (scheme_rest.BaseRestaurant): Specifie the restauranat

    Returns:
        db_models.Bewertung: Return one bewertung that match the restaurant - user
    """
    return (
        db.query(db_models.Bewertung)
        .join(db_models.Person, db_models.Person.email == db_models.Bewertung.person_email)
        .join(db_models.Restaurant, db_models.Restaurant.place_id == db_models.Bewertung.place_id)
        .filter(db_models.Person.email == user.email)
        .filter(db_models.Restaurant.place_id == rest.place_id)
        .first()
    )


def get_all_user_bewertungen(db: Session, user: scheme_user.UserBase) -> Union[List[db_models.Bewertung], None]:
    """Return all bewertugen from one User

    Args:
        db (Session): Session to the DB
        user (scheme_user.UserBase): The user to select

    Returns:
        List[db_models.Bewertung] OR None
    """
    user: db_models.Person = get_user_by_mail(db, user.email)
    if user is None:
        return None
    else:
        return user.bewertungen


def create_bewertung(db: Session, assessment: scheme_rest.RestBewertungCreate) -> db_models.Bewertung:
    """Create / Add a Bewertung to the DB. Timestamp and ID will set automatic.

    Args:
        db (Session): Session to the DB
        assessment (scheme_rest.RestBewertungCreate): Bewertung to add. This include the Person and Restaurant for the mapping of the Bewertung

    Returns:
        db_models.Bewertung: Return if success
    """
    if get_user_by_mail(db, assessment.person.email) is None:
        raise sqlalchemy.exc.InvalidRequestError("User does not exist")
    if get_restaurant_by_id(db, assessment.restaurant.place_id) is None:
        raise sqlalchemy.exc.InvalidRequestError("Restaurant does not exist")

    db_assessment = db_models.Bewertung(
        person_email=assessment.person.email,
        place_id=assessment.restaurant.place_id,
        kommentar=assessment.comment,
        rating=assessment.rating,
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


def update_bewertung(
    db: Session, old_bewertung: scheme_rest.RestBewertungCreate, new_bewertung: scheme_rest.RestBewertungCreate
) -> db_models.Bewertung:
    """Update the comment and rating of a bewertung

    Args:
        db (Session): Session to the DB
        old_bewertung (scheme_rest.RestBewertungCreate): The old Bewertung
        new_bewertung (scheme_rest.RestBewertungCreate): The updated Bewertung

    Returns:
        db_models.Bewertung: New Bewertung from `get_bewertung_from_user_to_rest`
    """
    (
        db.query(db_models.Bewertung)
        .filter(db_models.Bewertung.person_email == old_bewertung.person.email)
        .filter(db_models.Bewertung.place_id == old_bewertung.restaurant.place_id)
        .update(
            {db_models.Bewertung.kommentar: new_bewertung.comment, db_models.Bewertung.rating: new_bewertung.rating}
        )
    )
    db.commit()
    return get_bewertung_from_user_to_rest(db, new_bewertung.person, new_bewertung.restaurant)


def delete_bewertung(db: Session, user: scheme_user.User, rest: scheme_rest.BaseRestaurant) -> int:
    """Delete one Bewertung

    Args:
        db (Session): Session to the db
        user (scheme_user.User): The owner of the Bewertung
        rest (scheme_rest.BaseRestaurant): The corrosponding Restaurant

    Returns:
        int: Number of effected rows
    """
    rows = (
        db.query(db_models.Bewertung)
        .filter(db_models.Bewertung.person_email == user.email, db_models.Bewertung.place_id == rest.place_id)
        .delete()
    )
    db.commit()
    return rows


def create_user(db: Session, person: scheme_user.UserCreate) -> db_models.Person:
    """Create / Add Person to the Database with hashed password

    Args:
        db (Session): Session to the DB
        person (scheme_user.UserCreate): The person to create

    Returns:
        db_models.Person: Return the created person
    """
    db_person = db_models.Person(email=person.email, hashed_password=Hasher.get_password_hash(person.password))
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


def get_user_by_mail(db: Session, email: str) -> Union[db_models.Person, None]:
    """Get the person from the Databse if one found

    Args:
        db (Session): Session to the DB
        email (str): eMail to filter

    Returns:
        db_models.Person | None
    """
    return db.query(db_models.Person).filter(db_models.Person.email == email).first()


def update_user(db: Session, current_user: scheme_user.UserBase, new_user: scheme_user.UserCreate) -> db_models.Person:
    """Update the User in the Database. You can change the Mail or Password

    Args:
        db (Session): Session to the DB
        current_user (scheme_user.UserBase): User to Update
        new_user (scheme_user.UserCreate): Contains the updated values for the User

    Returns:
        db_models.Person: Return the new DB values
    """
    db_new_user = db_models.Person(email=new_user.email, hashed_password=Hasher.get_password_hash(new_user.password))
    db.query(db_models.Person).filter(db_models.Person.email == current_user.email).update(
        {db_models.Person.email: db_new_user.email, db_models.Person.hashed_password: db_new_user.hashed_password}
    )
    db.commit()
    return db_new_user


def delete_user(db: Session, user: scheme_user.UserBase) -> int:
    """Remove the Person with the given email

    Args:
        db (Session): Session to the DB
        email (str): Mail from the Person to search

    Returns:
        int: Number of effekted rows
    """
    rows = db.query(db_models.Person).filter(db_models.Person.email == user.email).delete()
    db.commit()
    return rows
