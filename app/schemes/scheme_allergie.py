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
    def allergie_values(cls, value: str) -> Any:
        """Check if the Allergie is in schemes.Allergies Enum

        Args:
            value (str): the name that got passed

        Returns:
            Any: Return a object if value is valid
        """
        for allergie in Allergies:
            if allergie.value == value:
                return value
        assert False, f"{value} is not a valid Allergie!"

    class Config:
        orm_mode = True
