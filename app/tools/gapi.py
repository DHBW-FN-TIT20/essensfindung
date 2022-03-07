"""Connection to the google api"""
from typing import List

import httpx

from schemes.exceptions import GoogleApiException
from schemes.scheme_filter import FilterRest
from schemes.scheme_rest import Restaurant
from tools.config import settings
from tools.my_logging import logger

# TODO: Asynchrone Funktionen
# TODO: Asynchrone API Anfragen


def search_restaurant(res_filter: FilterRest) -> List[Restaurant]:
    """Search all restaurants for a specific cuisin in a specific location

    Args:
        res_filter (schemes.scheme_filter.FilterRest): Filter for the API
    Raises:
        GoogleApiException: If something with the httpx went wrong

    Returns:
        List[schemes.scheme_rest.Restaurant]: List of all Restaurants from the google api
    """
    restaurants = []
    for cuisine in res_filter.cuisines:
        params: dict = {
            "keyword": cuisine.name,
            "location": f"{res_filter.location.lat},{res_filter.location.lng}",
            "opennow": True,
            "radius": res_filter.radius,
            "maxprice": res_filter.costs,
            "type": "restaurant",
            "language": "de",
        }

        try:
            restaurants.extend(nearby_search(params=params))
        except httpx.HTTPError as error:
            logger.exception(error)
            raise GoogleApiException("Can't communicate with the Google API") from error
    return restaurants


def nearby_search(params: dict, next_page_token: str = None) -> List[Restaurant]:
    """Specific google api request to search near a location for restaurants

    Args:
        params (dict): See all available params
            -> https://developers.google.com/maps/documentation/places/web-service/search-nearby#optional-parameters
        next_page_token (str, optional): For recursion if the result got more than 20 results you have to search with
            the next_page_token. Defaults to None.

    Returns:
        List[schemes.scheme_rest.Restaurant]: List of all found restaurants
    """
    url: str = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params["pagetoken"] = next_page_token
    params["key"] = settings.GOOGLE_API_KEY

    response = httpx.get(url, params=params)
    logger.debug("Response status: %s", response.status_code)
    logger.debug("Request url: %s", response.url)

    response.raise_for_status()

    resp_obj = response.json()
    restaurants = [Restaurant.parse_obj(restaurant) for restaurant in resp_obj.get("results")]

    if resp_obj.get("next_page_token"):
        restaurants.extend(nearby_search(params=params, next_page_token=resp_obj.get("next_page_token")))

    return restaurants


def place_details(restaurant: Restaurant) -> Restaurant:
    """To get additionals informations of a specifict place (restaurant) you have to do a specific api request

    Args:
        restaurant (schemes.scheme_rest.Restaurant): The Restaurant with the palce_id

    Returns:
        schemes.scheme_restRestaurant: The restaurant with all informations filled out if google got some
    """
    url: str = "https://maps.googleapis.com/maps/api/place/details/json"
    extended_restaurant: Restaurant = None

    params = {"key": settings.GOOGLE_API_KEY, "place_id": restaurant.place_id}
    response = httpx.get(url, params=params)
    logger.debug("Response status: %s", response.status_code)
    logger.debug("Request url: %s", response.url)

    response.raise_for_status()

    resp_obj = response.json().get("result")
    restaurant.homepage = resp_obj.get("website")
    restaurant.maps_url = resp_obj.get("url")
    restaurant.phone_number = resp_obj.get("international_phone_number")
    restaurant.geometry.location.adr = resp_obj.get("formatted_address")

    extended_restaurant = restaurant

    return extended_restaurant


def geocode(address: str) -> List[dict]:
    """This does geocoding (get information based on Streed addres / zipcode / plus code).

    Args:
        address (str): The street address or plus code that you want to geocode. Specify addresses in accordance with
            the format used by the national postal service of the country concerned.
            Additional address elements such as business names and unit, suite or floor numbers should be avoided.

    Raises:
        schemes.exceptions.GoogleApiException: Raises if no result found for the query

    Returns:
        List[dict]: Refer to the See Also

    References:
        https://developers.google.com/maps/documentation/geocoding/requests-geocoding

    """
    url: str = "https://maps.googleapis.com/maps/api/geocode/json"
    address = address.replace(" ", "%20")
    params = {"key": settings.GOOGLE_API_KEY, "address": address}

    response = httpx.get(url, params=params)
    logger.debug("Response status: %s", response.status_code)
    logger.debug("Request url: %s", response.url)

    response.raise_for_status()

    resp_obj = response.json().get("results")

    if len(resp_obj) == 0:
        raise GoogleApiException(f"No geocode result for query {address}")

    return resp_obj
