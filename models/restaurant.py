from pydantic import BaseModel, validator


class Location(BaseModel):
    lat: str
    lng: str
    adr: str = None


class Geometry(BaseModel):
    location: Location


class Restaurant(BaseModel):
    place_id: str
    name: str
    geometry: Geometry
    maps_url: str = None
    rating: float = 0
    own_rating: float = 0
    phone_number: str = None
    homepage: str = None
