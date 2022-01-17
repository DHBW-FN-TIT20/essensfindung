import logging
from typing import List

import httpx
from models.restaurant import Location, Restaurant

import infrastructure


# TODO: Asynchrone Funktionen
# TODO: Asynchrone API Anfragen

logger = logging.getLogger(__name__)


def search_restaurant(cuisin: infrastructure.Cuisine, location: Location, radius: int = 5000) -> List[Restaurant]:
    params: dict = {
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
    except Exception as error:
        logger.exception(error)
        raise error


def nearby_search(params: dict, next_page_token=None) -> List[Restaurant]:
    url: str = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params["pagetoken"] = next_page_token
    params["key"] = infrastructure.get_api_key()

    try:
        response = httpx.get(url, params=params)
        logger.debug(f"Response status: {response.status_code}")

        response.raise_for_status()

        resp_obj = response.json()
        restaurants = [Restaurant.parse_obj(restaurant) for restaurant in resp_obj.get("results")]

        if resp_obj.get("next_page_token"):
            restaurants.extend(nearby_search(params=params, next_page_token=resp_obj.get("next_page_token")))

    except httpx.HTTPError as error:
        raise error  # Vielleicht eigene exception machen

    return restaurants


def place_details(restaurants: list[Restaurant]) -> List[Restaurant]:
    url: str = "https://maps.googleapis.com/maps/api/place/details/json"
    extended_restaurants: List[Restaurant] = []
    try:
        for restaurant in restaurants:
            params = {"key": infrastructure.get_api_key(), "place_id": restaurant.place_id}
            response = httpx.get(url, params=params)
            logger.debug(f"Response status: {response.status_code}")

            response.raise_for_status()

            resp_obj = response.json().get("result")
            restaurant.homepage = resp_obj.get("website")
            restaurant.maps_url = resp_obj.get("url")
            restaurant.phone_number = resp_obj.get("international_phone_number")
            restaurant.geometry.location.adr = resp_obj.get("formatted_address")

            extended_restaurants.append(restaurant)
    except httpx.HTTPError as error:
        raise error

    return extended_restaurants
