"""Main Module for the Restaurant-Search"""
import random
from typing import List

from services import gapi
from schemes.filter import RestFilter
from schemes.scheme_rest import Restaurant


def search_for_restaurant(user_f: RestFilter) -> Restaurant:
    """Do a full search for a Restaurant. This does the google search, weights the result with the user rating
    and choose one of the restaurants according to the weights

    Args:
        user_f (RestFilter): Filter that are needed for the search

    Returns:
        Restaurant: The one choosen Restaurant where the user have to go now!
    """
    google_rests: List[Restaurant] = gapi.search_restaurant(user_f)
    filterd_rests: List[Restaurant] = filter_rating(google_rests, user_f.rating)
    user_rests: List[Restaurant] = fill_user_rating(filterd_rests)
    return select_restaurant(user_rests)


def fill_user_rating(rests: List[Restaurant]) -> List[Restaurant]:
    """Search in the connected DB if one restaurant got already rated from the user
    and if so add the value to the restaurant

    Args:
        google_res (List[Restaurant]): Restaurants for lookup

    Returns:
        List[Restaurant]: Return of the input List with the user rating if one got found
    """
    # TODO: No function at the moment
    # [ ] Fillup User rating if some are in the DB
    # [ ] Need User
    # [ ] Need DB Connection
    return rests


def filter_rating(rests: List[Restaurant], rating: int) -> List[Restaurant]:
    """Remove all Restaurants from the list under the given rating

    Args:
        rests (List[Restaurant]): List of all Restarants to filter
        rating (int): All under this number got removed

    Returns:
        List[Restaurant]: Filtered List based ob the rating
    """
    for res in rests:
        if res.rating < rating:
            rests.remove(res)
    return rests


def select_restaurant(rests: List[Restaurant]) -> Restaurant:
    """Select one restaurant with specific weight. weight = user_rating * 4 + google_rating * 2.
    If None rating found it will be count as 0

    Args:
        user_res (List[Restaurant]): The Rating of the Restaurants are optional

    Returns:
        Restaurant: The random chooses restaurant
    """
    weights: List[int] = []
    for res in rests:
        if res.own_rating is None:
            res.own_rating = 0
        if res.rating is None:
            res.rating = 0
        weights.append(res.own_rating * 4 + res.rating * 2)

    return random.choices(rests, weights=weights, k=1)[0]
