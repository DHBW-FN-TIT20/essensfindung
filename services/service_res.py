"""Main Module for the Restaurant-Search"""
import random
from typing import List

from infrastructure import gapi
from models.filter import RestFilter
from models.restaurant import Restaurant


def search_for_restaurant(user_f: RestFilter) -> Restaurant:
    """Do a full search for a Restaurant. This does the google search, weights the result with the user rating
    and choose one of the restaurants according to the weights

    Args:
        user_f (RestFilter): Filter that are needed for the search

    Returns:
        Restaurant: The one choosen Restaurant where the user have to go now!
    """
    google_res: List[Restaurant] = gapi.search_restaurant(user_f.cuisine, user_f.location, user_f.radius)
    user_res: List[Restaurant] = fill_user_rating(google_res)
    return select_restaurant(user_res)


def fill_user_rating(google_res: List[Restaurant]) -> List[Restaurant]:
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
    return google_res


def select_restaurant(user_res: List[Restaurant]) -> Restaurant:
    """Select one restaurant with specific weight. weight = user_rating * 4 + google_rating * 2.
    If None rating found it will be count as 0

    Args:
        user_res (List[Restaurant]): The Rating of the Restaurants are optional

    Returns:
        Restaurant: The random chooses restaurant
    """
    weights: List[int] = []
    for res in user_res:
        if res.own_rating is None:
            res.own_rating = 0
        if res.rating is None:
            res.rating = 0
        weights.append(res.own_rating * 4 + res.rating * 2)

    return random.choices(user_res, weights=weights, k=1)[0]
