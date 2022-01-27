"""Connection to the google api"""
import logging
from typing import List

import httpx
from schemes.scheme_rest import Restaurant, GoogleApiException
from schemes.scheme_filter import RestFilter

from configuration import config

# TODO: Asynchrone Funktionen
# TODO: Asynchrone API Anfragen

logger = logging.getLogger(__name__)


def search_restaurant(res_filter: RestFilter) -> List[Restaurant]:
    """Search all restaurants for a specific cuisin in a specific location

    Args:
        res_filter (RestFilter): Filter for the API
    Raises:
        GoogleApiException: If something with the httpx went wrong

    Returns:
        List[Restaurant]: List of all Restaurants from the google api
    """
    params: dict = {
        "keyword": res_filter.cuisine.value,
        "location": f"{res_filter.location.lat},{res_filter.location.lng}",
        "opennow": True,
        "radius": res_filter.radius,
        "maxprice": res_filter.costs,
        "type": "restaurant",
        "language": "de",
    }

    try:
        restaurants = nearby_search(params=params)
        restaurants = place_details(restaurants)
        return restaurants
    except httpx.HTTPError as error:
        logger.exception(error)
        raise GoogleApiException("Can't communicate with the Google API") from error


def nearby_search(params: dict, next_page_token: str = None) -> List[Restaurant]:
    """Specific google api request to search near a location for restaurants

    Args:
        params (dict): See all available params -> https://developers.google.com/maps/documentation/places/web-service/search-nearby#optional-parameters
        next_page_token (str, optional): For recursion if the result got more than 20 results you have to search with the next_page_token. Defaults to None.

    Returns:
        List[Restaurant]: List of all found restaurants
    """
    url: str = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params["pagetoken"] = next_page_token
    params["key"] = config.get_google_api_key()

    response = httpx.get(url, params=params)
    logger.debug("Response status: %s", response.status_code)
    logger.debug("Request url: %s", response.url)

    response.raise_for_status()

    resp_obj = response.json()
    restaurants = [Restaurant.parse_obj(restaurant) for restaurant in resp_obj.get("results")]

    if resp_obj.get("next_page_token"):
        restaurants.extend(nearby_search(params=params, next_page_token=resp_obj.get("next_page_token")))

    return restaurants


def place_details(restaurants: list[Restaurant]) -> List[Restaurant]:
    """To get additionals informations of a specifict place (restaurants) you have to do a specific api request

    Args:
        restaurants (list[Restaurant]): List of all Restaurants with the place_id in it

    Returns:
        List[Restaurant]: List of the restaurants with all informations filled out if google got some
    """
    url: str = "https://maps.googleapis.com/maps/api/place/details/json"
    extended_restaurants: List[Restaurant] = []
    for restaurant in restaurants:
        params = {"key": config.get_google_api_key(), "place_id": restaurant.place_id}
        response = httpx.get(url, params=params)
        logger.debug("Response status: %s", response.status_code)
        logger.debug("Request url: %s", response.url)

        response.raise_for_status()

        resp_obj = response.json().get("result")
        restaurant.homepage = resp_obj.get("website")
        restaurant.maps_url = resp_obj.get("url")
        restaurant.phone_number = resp_obj.get("international_phone_number")
        restaurant.geometry.location.adr = resp_obj.get("formatted_address")

        extended_restaurants.append(restaurant)

    return extended_restaurants
