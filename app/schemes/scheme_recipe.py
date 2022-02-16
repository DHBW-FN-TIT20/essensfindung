from datetime import timedelta
from typing import Optional

from pydantic import BaseModel


class Recipe(BaseModel):
    id: str
    name: str
    ingredients: str
    url: str
    image: Optional[str]
    cookTime: Optional[timedelta]
    prepTime: Optional[timedelta]
