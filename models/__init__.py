from enum import Enum


class Cuisine(Enum):
    """Only this Cuisine can be searched"""

    ITALIAN = "Italienisch"
    GERMAN = "Deutsch"
    ASIAN = "Asiatisch"
    DOENER = "Doener"
    TURKEY = "Tuerkisch"


class Allergies(Enum):
    """Filter for Allergies"""

    # TODO: More...
    LACTOSE = "lactose"
    WHEAT = "wheat"
