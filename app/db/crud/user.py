"""All DB functions for the User table"""
from typing import Union

from sqlalchemy.orm import Session

from db.base import Person
from schemes import scheme_user
from tools.hashing import Hasher


def create_user(db: Session, person: scheme_user.UserCreate) -> Person:
    """Create / Add Person to the Database with hashed password

    Args:
        db (Session): Session to the DB
        person (scheme_user.UserCreate): The person to create

    Returns:
        Person: Return the created person
    """
    db_person = Person(email=person.email, hashed_password=Hasher.get_password_hash(person.password))
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


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
    return rows
