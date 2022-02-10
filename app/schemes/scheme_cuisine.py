from pydantic import BaseModel
from pydantic import validator

from schemes import Cuisine


class PydanticCuisine(BaseModel):
    """Needed class for revonvert orm models"""

    name: str

    @classmethod
    @validator("name")
    def allergie_values(cls, value: str):
        """Check if the cuisine is in schemes.Cuisine Enum"""
        for cuisine in Cuisine:
            if cuisine.value == value:
                return value
        assert False, f"{value} is not a valid Cuisine!"

    class Config:
        orm_mode = True
