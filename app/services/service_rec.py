from typing import List
from typing import Union

import pandas
from sqlalchemy.orm import Session

from db.crud import recipeBewertung as crud_recipeBewertung
from schemes.exceptions import DatabaseException
from schemes.exceptions import RecipeNotFound
from schemes.scheme_filter import FilterRecipe
from schemes.scheme_recipe import Recipe
from schemes.scheme_recipe import RecipeBase
from schemes.scheme_recipe import RecipeBewertungCreate
from schemes.scheme_recipe import RecipeBewertungReturn
from schemes.scheme_user import UserBase
from tools.recipe_db import recipe_db
from tools.recipe_db import RecipeDB


def search_recipe(db_session: Session, user: UserBase, recipe_filter: FilterRecipe) -> Recipe:
    """Search for a recipe with the given filter

    Args:
        db_session (sqlalchemy.orm.Session): Session to the DB -> See `db: Session = Depends(get_db)`
        recipe_filter (schemes.scheme_filter.FilterRecipe): Filter the Recipes

    Returns:
        schemes.scheme_recipe.Recipe: The one choosen Recipe
    """
    pd_random_recipe: pandas.DataFrame = __apply_filter(recipe_db.pd_frame, recipe_filter).sample()
    random_recipe = Recipe(
        id=pd_random_recipe["_id.$oid"].array[0],
        name=pd_random_recipe["name"].array[0],
        ingredients=pd_random_recipe["ingredients"].array[0],
        url=pd_random_recipe["url"].array[0],
        image=pd_random_recipe["image"].array[0],
        cookTime=pd_random_recipe["cookTime"].array[0],
        prepTime=pd_random_recipe["prepTime"].array[0],
    )

    if not crud_recipeBewertung.get_bewertung_from_user_to_recipe(db=db_session, user=user, recipe=random_recipe):
        add_assessment(
            db_session=db_session,
            assessment=RecipeBewertungCreate(name=random_recipe.name, person=user, recipe=random_recipe),
        )

    return random_recipe


def __apply_filter(recipes: pandas.DataFrame, recipe_filter: FilterRecipe) -> pandas.DataFrame:
    cooktime_bool = RecipeDB.filter_cooktime(user_pd_frame=recipes, total_time=recipe_filter.total_time)
    keyword_bool = RecipeDB.filter_keyword(user_pd_frame=recipes, keyword=recipe_filter.keyword)
    filter_bool = cooktime_bool & keyword_bool

    if not (True in filter_bool.value_counts()):
        raise RecipeNotFound("No Recipe Found with these Filters")

    return recipes[filter_bool]


def get_assessments_from_user(db_session: Session, user: UserBase) -> Union[List[RecipeBewertungReturn], None]:
    """Get Bewertungen from a User to all recipes

    Args:
        db_session (sqlalchemy.orm.Session): Session to the DB -> See `db: Session = Depends(get_db)`
        user_mail (str): Mail of the User

    Returns:
        Union[List[schemes.scheme_recipe.RecipeBewertungReturn], None]: Return a List of all Recipe or None
    """
    db_recipes = crud_recipeBewertung.get_all_user_bewertungen(db_session, user)
    scheme_recipes = [
        RecipeBewertungReturn(
            name=db_recipe.rezept_name,
            email=db_recipe.person_email,
            id=db_recipe.rezept_id,
            comment=db_recipe.kommentar,
            rating=db_recipe.rating,
            timestamp=db_recipe.zeitstempel,
        )
        for db_recipe in db_recipes
    ]
    return scheme_recipes


def add_assessment(db_session: Session, assessment: RecipeBewertungCreate) -> RecipeBewertungReturn:
    """Add the given assessment to the Database.

    Args:
        db_session (sqlalchemy.orm.Session): Session to the DB -> See `db: Session = Depends(get_db)`
        assessment (schemes.scheme_recipe.RecipeBewertungCreate): The assessment need to be unique

    Raises:
        schemes.exceptions.DatabaseException: if the User or Recipe does not exist or the assessment is duplicated

    Returns:
        [schemes.scheme_recipe.RecipeBewertungReturn]: The created recipe
    """
    try:
        created_assessment = crud_recipeBewertung.create_bewertung(db_session, assessment)
        return RecipeBewertungReturn(
            name=created_assessment.rezept_name,
            email=created_assessment.person_email,
            id=created_assessment.rezept_id,
            comment=created_assessment.kommentar,
            rating=created_assessment.rating,
            timestamp=created_assessment.zeitstempel,
        )
    except DatabaseException as error:
        raise error


def update_assessment(
    db_session: Session, old_assessment: RecipeBewertungCreate, new_assessment: RecipeBewertungCreate
) -> RecipeBewertungReturn:
    """Update the comment and rating of a existing assessment

    Args:
        db_session (sqlalchemy.orm.Session): Session to the DB -> See `db: Session = Depends(get_db)`
        old_assessment (schemes.scheme_recipe.RestBewertungCreate): The current assessment
        new_assessment (schemes.scheme_recipe.RecipeBewertungCreate): The new assessment with the updated values

    Raises:
        schemes.exceptions.DatabaseException: if the User or Recipe does not exist

    Returns:
        schemes.scheme_recipe.RecipeBewertungReturn: Recipe with the new values
    """
    try:
        updated_assessment = crud_recipeBewertung.update_assessment(db_session, old_assessment, new_assessment)
    except DatabaseException as error:
        raise error
    return RecipeBewertungReturn(
        name=updated_assessment.rezept_name,
        email=updated_assessment.person_email,
        id=updated_assessment.rezept_id,
        comment=updated_assessment.kommentar,
        rating=updated_assessment.rating,
        timestamp=updated_assessment.zeitstempel,
    )


def delete_assessment(db_session: Session, user: UserBase, recipe: RecipeBase) -> int:
    """Delete one assessment that are mapped between the user and recipe

    Args:
        db_session (sqlalchemy.orm.Session): Session to the DB -> See `db: Session = Depends(get_db)`
        user (schemes.scheme_user.UserBase): The owner of the assessment
        recipe (schemes.scheme_recipe.RecipeBase): The mapped recipe

    Raises:
        schemes.exceptions.DatabaseException: if the User or recipe does not exist

    Returns:
        int: The number of affected Rows of the delete
    """
    rows = crud_recipeBewertung.delete_bewertung(db_session, user, recipe)
    if rows == 0:
        raise DatabaseException("Can not delete assessment. Does the user and recipe excist?")
    return rows
