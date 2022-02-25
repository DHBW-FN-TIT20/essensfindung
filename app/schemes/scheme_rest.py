""" Contains all classes for the restaurant search """
import datetime
from typing import Optional

from pydantic import BaseModel

from . import scheme_user


class LocationBase(BaseModel):
    """
    contain only coordinates

    Attributes:
        lat (str): Latitude
        lng (str): Longitude
    """

    lat: str
    lng: str


class LocationRest(LocationBase):
    """
    Store further information about the location of the restaurant

    Attributes:
        adr (str): Address of the Restaurant. Defaults to None
    """

    adr: str = None


class Geometry(BaseModel):
    """
    Needed for better automation converting from the google api

    Attributes:
        location (schemes.scheme_rest.LocationRest)
    """

    location: LocationRest


class RestaurantBase(BaseModel):
    """
    Scheme that is only needed for the DB

    Attributes:
        place_id (str): ID from Google
        name (str): Name of the Restaurant
    """

    place_id: str
    name: str


class RestaurantCreate(RestaurantBase):
    """
    Scheme that is only needed for the DB

    Attributes:
        name (str): Name of the Restaurant
    """

    name: str

    class Config:
        orm_mode = True


class Restaurant(RestaurantBase):
    """
    Class that got return to the website

    Attributes:
        name (str): Name of the Restaurant
        geometry (Geometry): Postion of the Restaurant
        maps_url (str): google maps url of the restaurant. Defaults to None.
        rating (float): google rating. Defaults. to None
        own_rating (float): User rating. Defgaults to None.
        phone_number (str): Phonenumber of the restaurant. Defgaults to None.
        homepage (str): Url of the homepage. Defgaults to None.
    """

    name: str
    geometry: Geometry
    maps_url: str = None
    rating: float = None
    own_rating: float = None
    phone_number: str = None
    homepage: str = None


class RestBewertungBase(BaseModel):
    """
    BaseClass for the Bewertung

    Attributes:
        name (str): Name of the restaurant
        comment (Optional[str]): comment from the user. Defaults to "".
        rating (Optional[float]): Rating of the user. Defaults to 0.
    """

    name: str
    comment: Optional[str] = ""
    rating: Optional[float] = 0


class RestBewertungCreate(RestBewertungBase):
    """
    Class to create a new Bewertung in the DB

    Attributes:
        person (scheme_user.UserBase): Owner of the assessment.
        restaurant (RestaurantBase): The restaurant.
    """

    person: scheme_user.UserBase
    restaurant: RestaurantBase


class RestBewertungReturn(RestBewertungBase):
    """
    Class to return to the frontend

    Attributes:
        email (str): Email of the User
        place_id (str): PlaceID of the Restaurant
        timestamp (datetime.datetime): Last Update of the assessment
    """

    email: str
    place_id: str
    timestamp: datetime.datetime

    class Config:
        orm_mode = True
