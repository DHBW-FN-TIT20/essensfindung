"""Contains all Models and Classes for the Application"""
from enum import Enum


class Cuisine(Enum):
    """Only this Cuisine can be searched"""

    ITALIAN = "Italienisch"
    GERMAN = "Deutsch"
    ASIAN = "Asiatisch"
    DOENER = "Doener"
    TURKEY = "Tuerkisch"
    GREEK = "Griechisch"
    KOREAN = "Koreanisch"
    THAILAND = "Thailaendisch"
    INDIAN = "Indisch"
    COFFE = "Kaffee"
    BAKERY = "Baecker"
    BUTCHER = "Metzger"


class Allergies(Enum):
    """Filter for Allergies"""

    # TODO: More...
    LACTOSE = "Laktoseintoleranz"
    WHEAT = "Glutenunvertraeglichkeit"
