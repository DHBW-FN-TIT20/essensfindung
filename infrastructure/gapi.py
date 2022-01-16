import logging
from typing import List

import requests
from models.restaurant import Location, Restaurant

import infrastructure


def search_restaurant(cuisin: infrastructure.Cuisine, location: Location, radius: int = 5000) -> List[Restaurant]:
    params: dict = {
        "key": infrastructure.get_api_key(),
        "keyword": cuisin.value,
        "location": f"{location.lat},{location.lng}",
        "opennow": True,
        "radius": radius,
        "type": "restaurant",
        "language": "de",
    }

    try:
        restaurants = nearby_search(params=params)
        restaurants = place_details(restaurants)
    except requests.HTTPError as error:
        logging.error("Cant request Restaurant from Google API")
        raise error


def nearby_search(params: dict) -> List[Restaurant]:
    url: str = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    try:
        # TODO: Checken ob es noch einen next_page_token gibt  - https://developers.google.com/maps/documentation/places/web-service/search-nearby#PlacesNearbySearchResponse-next_page_token
        response = requests.get(url, params=params)
        response.raise_for_status()

        resp_obj = response.json().get("results")
        restaurants = [Restaurant.parse_obj(restaurant) for restaurant in resp_obj]
        pass
    except Exception as error:
        logging.exception(error)
        raise error  # Vielleicht eigene exception machen

    return restaurants


def place_details(restaurants: list[Restaurant]) -> List[Restaurant]:
    url: str = "https://maps.googleapis.com/maps/api/place/details/json"
    extended_restaurants: List[Restaurant] = []
    try:
        for restaurant in restaurants:
            params = {"key": infrastructure.get_api_key(), "place_id": restaurant.place_id}
            response = requests.get(url, params=params)
            response.raise_for_status()

            resp_obj = response.json().get("result")
            restaurant.homepage = resp_obj.get("website")
            restaurant.maps_url = resp_obj.get("url")
            restaurant.phone_number = resp_obj.get("international_phone_number")
            restaurant.geometry.location.adr = resp_obj.get("formatted_address")

            extended_restaurants.append(restaurant)
    except Exception as error:
        logging.exception(error)
        raise error

    return extended_restaurants
