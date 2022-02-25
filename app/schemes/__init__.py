"""Contains all Models and Classes for the Application"""
from enum import Enum


class Cuisine(Enum):
    """
    Only this Cuisine can be searched

    Attributes:
        ITALIAN
        GERMAN
        ASIAN
        DOENER
        TURKEY
        GREEK
        KOREAN
        THAILAND
        INDIAN
        COFFE
        BAKERY
        BUTCHER
        VEGAN
        VEGETARIAN
        FASTFOOD
        AMERICAN
        RESTAURANT
    """

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
    BUTCHER = "Metzgerei"
    VEGAN = "Vegan"
    VEGETARIAN = "Vegetarisch"
    FASTFOOD = "Fastfood"
    AMERICAN = "Amerikanisch"
    RESTAURANT = "Restaurant"  # used when no cuisine is selected


class Allergies(Enum):
    """
    Filter for Allergies

    Attributes:
        LACTOSE (str): Defaults to Laktoseintoleranz
        WHEAT (str): Defaults to Glutenunvertraeglichkeit

    """

    # TODO: More...
    LACTOSE = "Laktoseintoleranz"
    WHEAT = "Glutenunvertraeglichkeit"
