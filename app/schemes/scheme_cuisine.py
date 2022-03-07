"""Class for the Cuisine"""
from pydantic import BaseModel
from pydantic import validator

from schemes import Cuisine


class PydanticCuisine(BaseModel):
    """
    Needed class for revonvert orm models

    Attributes:
        name (str): Only schemes.Cuisine Enum valid
    """

    name: str

    @validator("name")
    def cuisine_values(cls, value: str):
        """
        Check if the cuisine is in schemes.cuisines Enum

        Args:
            cls (any): Class of the method
            value (str): the name that got passed

        Returns:
            Any: Return a object if value is valid
        """
        for cuisine in Cuisine:
            if cuisine.value == value:
                return value
        assert False, f"{value} is not a valid Cuisine!"

    class Config:
        orm_mode = True
