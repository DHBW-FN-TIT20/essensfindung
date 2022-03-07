"""Class for the Allergies"""
from typing import Any

from pydantic import BaseModel
from pydantic import validator

from schemes import Allergies


class PydanticAllergies(BaseModel):
    """Needed class for revonvert orm models

    Attributes:
        name (str): Only Schemes in the schemes.Allergies Enum are valid
    """

    name: str

    @validator("name")
    @classmethod
    def allergie_values(cls, value: str):
        """Check if the Allergie is in schemes.Allergies Enum

        Args:
            value (str): the name that got passed
        """
        for allergie in Allergies:
            if allergie.value == value:
                return value
        assert False, f"{value} is not a valid Allergie!"

    class Config:
        orm_mode = True
