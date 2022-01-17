""" Contains all classes for the restaurant search """
from pydantic import BaseModel


class Location(BaseModel):
    """store further information about the location of the restaurant"""

    lat: str
    lng: str
    adr: str = None


class Geometry(BaseModel):
    """Needed for better automation converting from the google api"""

    location: Location


class Restaurant(BaseModel):
    """Basse class that got return to the website"""

    place_id: str
    name: str
    geometry: Geometry
    maps_url: str = None
    rating: float = None
    own_rating: float = None
    phone_number: str = None
    homepage: str = None


class GoogleApiException(Exception):
    """Exception if some Error from the Google API request are made"""
