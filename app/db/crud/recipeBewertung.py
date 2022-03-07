"""All DB functions for the Bewertung table"""
from typing import List
from typing import Union

import sqlalchemy
from sqlalchemy.orm import Session

from db.base import BewertungRecipe
from db.base import Person
from db.crud.user import get_user_by_mail
from schemes import scheme_recipe
from schemes import scheme_user
from schemes.exceptions import DatabaseException
from schemes.exceptions import DuplicateEntry
from schemes.exceptions import UserNotFound
from tools.my_logging import logger


def get_bewertung_from_user_to_recipe(
    db: Session, user: scheme_user.UserBase, recipe: scheme_recipe.RecipeBase
) -> BewertungRecipe:
    """Return a specific bewertung from a user to only one recipe

    Args:
        db (Session): Session to the DB
        user (scheme_user.UserBase): Specifie the User
        recipe (scheme_recipe.RecipeBase): Specifie the reciepe

    Returns:
        BewertungRecipe: Return one bewertung that match the recipe - user
    """
    return (
        db.query(BewertungRecipe)
        .join(Person, Person.email == BewertungRecipe.person_email)
        .filter(Person.email == user.email)
        .filter(BewertungRecipe.rezept_id == recipe.id)
        .first()
    )


def get_all_user_bewertungen(db: Session, user: scheme_user.UserBase) -> Union[List[BewertungRecipe], None]:
    """Return all bewertugen from one to the recipes User

    Args:
        db (Session): Session to the DB
        user (scheme_user.UserBase): The user to select

    Returns:
        Union[List[BewertungRecipe], None]
    """
    user: Person = get_user_by_mail(db, user.email)
    if user is None:
        return None
    else:
        return user.bewertungenRezept


def create_bewertung(db: Session, assessment: scheme_recipe.RecipeBewertungCreate) -> BewertungRecipe:
    """Create / Add a Bewertung to the DB. Timestamp and ID will set automatic.

    Args:
        db (Session): Session to the DB
        assessment (scheme_recipe.RecipeBewertungCreate): Bewertung to add. This include the
            Person and Recipe for the mapping of the Bewertung

    Raises:
        UserNotFound: If the user does not exist
        DuplicateEntry: Duplicate Primary Key

    Returns:
        BewertungRecipe: Return if success
    """
    if get_user_by_mail(db, assessment.person.email) is None:
        raise UserNotFound(f"User {assessment.person.email} does not exist", assessment.person.email)

    db_assessment = BewertungRecipe(
        person_email=assessment.person.email,
        rezept_id=assessment.recipe.id,
        rezept_name=assessment.name,
        kommentar=assessment.comment,
        rating=assessment.rating,
    )
    try:
        db.add(db_assessment)
        db.commit()
        db.refresh(db_assessment)
        logger.info(
            "Added assessment to db... recipe id:%s\temail:%s\trating:%s\tcomment:%s",
            db_assessment.rezept_id,
            db_assessment.person_email,
            db_assessment.rating,
            db_assessment.kommentar,
        )
        return db_assessment
    except sqlalchemy.exc.IntegrityError as error:
        raise DuplicateEntry("Assessment already exist") from error


def update_assessment(
    db: Session, old_bewertung: scheme_recipe.RecipeBewertungCreate, new_bewertung: scheme_recipe.RecipeBewertungCreate
) -> BewertungRecipe:
    """Update the comment and rating of a bewertung

    Args:
        db (Session): Session to the DB
        old_bewertung (scheme_recipe.RecipeBewertungCreate): The old Bewertung
        new_bewertung (scheme_recipe.RecipeBewertungCreate): The updated Bewertung

    Returns:
        BewertungRecipe: New Bewertung from `get_bewertung_from_user_to_recipe`
    """
    rows = (
        db.query(BewertungRecipe)
        .filter(BewertungRecipe.person_email == old_bewertung.person.email)
        .filter(BewertungRecipe.rezept_id == old_bewertung.recipe.id)
        .update({BewertungRecipe.kommentar: new_bewertung.comment, BewertungRecipe.rating: new_bewertung.rating})
    )

    if rows == 0:
        raise DatabaseException("Can not update assessment. Does the User and the Recipe exist?")

    db.commit()
    logger.info("Updated bewertung %s - %s", old_bewertung.person.email, old_bewertung.recipe.id)
    return get_bewertung_from_user_to_recipe(db, new_bewertung.person, new_bewertung.recipe)


def delete_bewertung(db: Session, user: scheme_user.UserBase, recipe: scheme_recipe.RecipeBase) -> int:
    """Delete one Bewertung

    Args:
        db (Session): Session to the db
        user (scheme_user.User): The owner of the Bewertung
        recipe (scheme_recipe.RecipeBase): The corrosponding Recipe

    Returns:
        int: Number of effected rows
    """
    rows = (
        db.query(BewertungRecipe)
        .filter(BewertungRecipe.person_email == user.email, BewertungRecipe.rezept_id == recipe.id)
        .delete()
    )
    db.commit()
    logger.info("Deleted bewertung %s - %s", user.email, recipe.id)
    return rows
