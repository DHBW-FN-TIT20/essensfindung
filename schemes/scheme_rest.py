""" Contains all classes for the restaurant search """
from pydantic import BaseModel


class BaseLocation(BaseModel):
    """contain only coordinates"""

    lat: str
    lng: str


class ResLocation(BaseLocation):
    """store further information about the location of the restaurant"""

    adr: str = None


class Geometry(BaseModel):
    """Needed for better automation converting from the google api"""

    location: ResLocation


class BaseRestaurant(BaseModel):
    """Scheme that is only needed for the DB"""

    place_id: str

    class Config:
        orm_mode = True


class Restaurant(BaseRestaurant):
    """Class that got return to the website"""

    name: str
    geometry: Geometry
    maps_url: str = None
    rating: float = None
    own_rating: float = None
    phone_number: str = None
    homepage: str = None


class BaseRestBewertung(BaseModel):
    """Class to create Bewertungen for the DB"""

    comment: str
    rating: float


class RestBewertung(BaseRestBewertung):
    """Class to return a Bewertung"""
    timestamp: str

    class Config:
        orm_mode = True


class GoogleApiException(Exception):
    """Exception if some Error from the Google API request are made"""
