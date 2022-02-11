from datetime import timedelta

from pydantic import BaseModel


class Recipe(BaseModel):
    id: str
    name: str
    ingredients: str
    url: str
    image: str
    cookTime: timedelta
    prepTime: timedelta
