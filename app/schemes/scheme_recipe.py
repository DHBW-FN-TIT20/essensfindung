"""Contains the Class for Recipe"""
from datetime import timedelta
from typing import Optional

from pydantic import BaseModel


class Recipe(BaseModel):
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

    id: str
    name: str
    ingredients: str
    url: str
    image: Optional[str]
    cookTime: Optional[timedelta]
    prepTime: Optional[timedelta]
