"""Contains the Class for Recipe"""
import datetime
from datetime import timedelta
from typing import Optional

from pydantic import BaseModel

from schemes import scheme_user


class RecipeBase(BaseModel):
    """Base class for the Recipes

    Attributes:
        id (str): id of the recipe
    """

    id: str


class Recipe(RecipeBase):
    """
    Class that you get from the backend to handle the recipe

    Attributes:
        id (str): id of the recipe
        name (str): name of the recipe
        ingredients (str): ingredients of the recipe
        url (str): url to the original page of the recipe
        image (Optional[str]): url to an image if db contain one
        cookTime (Optional[timedelta]): cooktime of the recipe if specified
        prepTime (Optional[timedelta]): preperation time of the recipe if specified
    """

    name: str
    ingredients: str
    url: str
    image: Optional[str]
    cookTime: Optional[timedelta]
    prepTime: Optional[timedelta]


class RecipeBewertungBase(BaseModel):
    """
    BaseClass for the Bewertung

    Attributes:
        name (str): Name of the restaurant
        comment (Optional[str]): comment from the user. Defaults to "".
        rating (Optional[float]): Rating of the user. Defaults to 0.
    """

    name: str
    comment: Optional[str] = ""
    rating: Optional[float] = 0


class RecipeBewertungCreate(RecipeBewertungBase):
    """
    Class to create a new Bewertung in the DB

    Attributes:
        person (scheme_user.UserBase): Owner of the assessment.
        recipe (scheme_recipe.RecipeBase): The recipe.
    """

    person: scheme_user.UserBase
    recipe: RecipeBase


class RecipeBewertungReturn(RecipeBewertungBase):
    """
    Class to return to the frontend

    Attributes:
        email (str): Email of the User
        id (str): PlaceID of the recipe
        timestamp (datetime.datetime): Last Update of the assessment
    """

    email: str
    id: str
    timestamp: datetime.datetime

    class Config:
        orm_mode = True
