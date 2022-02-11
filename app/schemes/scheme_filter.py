"""Contains all Filter for the searches"""
from datetime import timedelta
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import validator

from .scheme_rest import LocationBase
from schemes import scheme_allergie
from schemes import scheme_cuisine


class FilterBase(BaseModel):
    """Base Filter for recepes and restaurant"""

    cuisines: List[scheme_cuisine.PydanticCuisine]
    allergies: Optional[List[scheme_allergie.PydanticAllergies]] = None
    rating: int

    @validator("rating")
    @classmethod
    def rating_range(cls, value: int) -> int:
        """Check if rating >= 1 and <= 5

        Args:
            value (int): Value of rating

        Raises:
            ValueError: If wrong values
        """
        if 1 <= value <= 5:
            return value
        raise ValueError("rating is not between 1 (included) and 5 (included)")


class FilterRest(FilterBase):
    """Use this scheme to Search for a Restaurant in the Backend"""

    costs: int
    radius: int
    location: LocationBase

    @validator("costs")
    @classmethod
    def costs_range(cls, value: int):
        """Check if costs >= 0 and <= 4

        Args:
            value (int): Value of costs

        Raises:
            ValueError: If wrong values
        """
        if 0 <= value <= 4:
            return value
        raise ValueError("costs is not between 0 (included) and 4 (included)")


class FilterRestDatabase(FilterBase):
    """Use this scheme if you internact with the Filter that are saved in the DB"""

    costs: int
    radius: int
    zipcode: str

    class Config:
        orm_mode = True

    @validator("costs")
    @classmethod
    def costs_range(cls, value: int):
        """Check if costs >= 0 and <= 4

        Args:
            value (int): Value of costs

        Raises:
            ValueError: If wrong values
        """
        if 0 <= value <= 4:
            return value
        raise ValueError("costs is not between 0 (included) and 4 (included)")

    @validator("zipcode")
    @classmethod
    def plz_length(cls, value: str):
        """Check if the zipcode got the length 5

        Args:
            value (int): Value of zipcode

        Raises:
            ValueError: If wrong value
        """
        if len(value) == 5:
            return value
        raise ValueError("costs is not between 0 (included) and 4 (included)")


class FilterRecipe(FilterBase):
    """Extended Model for Recipe-Filter"""

    totalTime: timedelta
