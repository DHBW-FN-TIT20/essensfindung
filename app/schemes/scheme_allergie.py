from pydantic import BaseModel
from pydantic import constr
from pydantic import validator

from schemes import Allergies


class PydanticAllergies(BaseModel):
    """Needed class for revonvert orm models"""

    name: str

    @classmethod
    @validator("name")
    def allergie_values(cls, value: str):
        """Check if the Allergie is in schemes.Allergies Enum"""
        for allergie in Allergies:
            if allergie.value == value:
                return value
        assert False, f"{value} is not a valid Allergie!"

    class Config:
        orm_mode = True
