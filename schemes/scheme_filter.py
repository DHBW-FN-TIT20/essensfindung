"""Contains all Filter for the searches"""
from pydantic import BaseModel, validator
from schemes import Cuisine, Allergies
from .scheme_rest import BaseLocation


class BaseFilter(BaseModel):
    """Base Filter for recepes and restaurant"""

    cuisine: Cuisine
    allergies: Allergies
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


class RestFilter(BaseFilter):
    """Use this scheme to Search for a Restaurant in the Backend"""

    costs: int
    radius: int
    location: BaseLocation

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


class DBFilter(BaseFilter):
    """Use this scheme if you internact with the Filter that are saved in the DB"""

    costs: int
    radius: int
    zipcode: str

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


class RecipeFilter(BaseFilter):
    """Extended Model for Recipe-Filter"""

    difficulty: int

    @validator("difficulty")
    @classmethod
    def difficulty_range(cls, value: int):
        """Check if difficulty >= 1 and <= 5

        Args:
            value (int): Value of difficulty

        Raises:
            ValueError: If wrong values
        """
        if 1 <= value <= 5:
            return value
        raise ValueError("difficulty is not between 1 (included) and 5 (included)")
