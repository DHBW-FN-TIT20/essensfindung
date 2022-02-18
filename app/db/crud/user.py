"""All DB functions for the User table"""
from typing import Union

import sqlalchemy
from sqlalchemy.orm import Session

from db.base import Person
from schemes import scheme_user
from schemes.exceptions import DuplicateEntry
from schemes.exceptions import UserNotFound
from tools.hashing import Hasher
from tools.my_logging import logger


def create_user(db: Session, person: scheme_user.UserCreate) -> Person:
    """Create / Add Person to the Database with hashed password

    Args:
        db (Session): Session to the DB
        person (scheme_user.UserCreate): The person to create

    Raises:
        DuplicateEntry: Duplicate Primary Key

    Returns:
        Person: Return the created person
    """
    try:
        db_person = Person(email=person.email, hashed_password=Hasher.get_password_hash(person.password))
        db.add(db_person)
        db.commit()
        db.refresh(db_person)

        logger.info("Added User to db... user:%s", db_person.email)

        return db_person
    except sqlalchemy.exc.IntegrityError as error:
        raise DuplicateEntry(f"User {person.email} already exist") from error


def get_user_by_mail(db: Session, email: str) -> Union[Person, None]:
    """Get the person from the Databse if one found

    Args:
        db (Session): Session to the DB
        email (str): eMail to filter

    Returns:
        Person | None
    """
    return db.query(Person).filter(Person.email == email).first()


def update_user(db: Session, current_user: scheme_user.UserBase, new_user: scheme_user.UserCreate) -> Person:
    """Update the User in the Database. You can change the Mail or Password

    Args:
        db (Session): Session to the DB
        current_user (scheme_user.UserBase): User to Update
        new_user (scheme_user.UserCreate): Contains the updated values for the User

    Returns:
        Person: Return the new DB values
    """
    db_new_user = Person(email=new_user.email, hashed_password=Hasher.get_password_hash(new_user.password))
    db.query(Person).filter(Person.email == current_user.email).update(
        {Person.email: db_new_user.email, Person.hashed_password: db_new_user.hashed_password}
    )
    db.commit()

    logger.info("Updated User... (old)email:%s", current_user.email)

    return db_new_user


def delete_user(db: Session, user: scheme_user.UserBase) -> int:
    """Remove the Person with the given email

    Args:
        db (Session): Session to the DB
        email (str): Mail from the Person to search

    Returns:
        int: Number of effekted rows
    """
    rows = db.query(Person).filter(Person.email == user.email).delete()
    db.commit()

    if rows == 0:
        raise UserNotFound(f"Can not delete User {user.email} - NotFound", user.email)

    logger.info("Delete User from db... email:%s", user.email)

    return rows
