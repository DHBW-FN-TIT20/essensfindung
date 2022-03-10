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
    """
    Base Filter for recepes and restaurant

    Attributes:
        cuisines (List[scheme_cuisine.PydanticCuisine]): All cuisines to search
        rating (int): Minimum rating
        allergies (Optional[List[scheme_allergie.PydanticAllergies]]): All allergies to take care of
    """

    cuisines: List[scheme_cuisine.PydanticCuisine]
    rating: int
    allergies: Optional[List[scheme_allergie.PydanticAllergies]]

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
    """
    Use this scheme to Search for a Restaurant in the Backend

    Attributes:
        costs (int): Maximum pricing
        radius (int): Radius of the search
        location (schemes.scheme_rest.LocationBase): Position for the search
    """

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
    """
    Use this scheme if you internact with the Filter that are saved in the DB

    Attributes:
        costs (int): Maximum pricing
        radius (int): Radius of the search
        manuell_location (str): To save the location

    """

    costs: int
    radius: int
    manuell_location: str

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


class FilterRecipe(BaseModel):
    """
    Extended Model for Recipe-Filter

    Attributes:
        keyword (str): Keyword to search
        total_time (datetime.timedelta): Max cook time
    """

    keyword: str
    total_time: timedelta
