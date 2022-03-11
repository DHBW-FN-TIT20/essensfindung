"""Main Module for the Restaurant-Search"""
import random
from typing import List
from typing import Union

import httpx
from sqlalchemy.orm import Session

from db.crud import filter as crud_filter
from db.crud import restaurant as crud_restaurant
from db.crud import restBewertung as crud_restBewertung
from schemes.exceptions import DatabaseException
from schemes.exceptions import DuplicateEntry
from schemes.exceptions import GoogleApiException
from schemes.exceptions import NoneExcistingLocationException
from schemes.exceptions import NoResultsException
from schemes.exceptions import UserNotFound
from schemes.scheme_filter import FilterRest
from schemes.scheme_filter import FilterRestDatabase
from schemes.scheme_rest import LocationBase
from schemes.scheme_rest import Restaurant
from schemes.scheme_rest import RestaurantBase
from schemes.scheme_rest import RestBewertungCreate
from schemes.scheme_rest import RestBewertungReturn
from schemes.scheme_user import UserBase
from tools import gapi


def get_coordinates_from_location(location: str) -> LocationBase:
    """Convert a string containing an address into coordinates

    Args:
        location (str): The address/zipcode string to search

    Raises:
        NoneExcistingLocationException: Raises if the location was not found

    Returns:
        schemes.scheme_rest.LocationBase: Location with the coordinates
    """
    try:
        results = gapi.geocode(location)
        location = results[0].get("geometry").get("location")
        return LocationBase(**location)
    except GoogleApiException as error:
        raise NoneExcistingLocationException(f"Invalid location {location} - no results") from error


def get_assessments_from_user(db_session: Session, user: UserBase) -> Union[List[RestBewertungReturn], None]:
    """Get Bewertungen from a User to all restaurants

    Args:
        db_session (sqlalchemy.orm.Session): Session to the DB -> See `db: Session = Depends(get_db)`
        user_mail (str): Mail of the User

    Returns:
        Union[List[schemes.scheme_rest.RestBewertungReturn], None]: Return a List of all Restaurants or None
    """
    db_rests = crud_restBewertung.get_all_user_bewertungen(db_session, user)
    scheme_rests = [
        RestBewertungReturn(
            name=db_rest.restaurant.name,
            email=db_rest.person_email,
            place_id=db_rest.place_id,
            comment=db_rest.kommentar,
            rating=db_rest.rating,
            timestamp=db_rest.zeitstempel,
        )
        for db_rest in db_rests
    ]
    return scheme_rests


def add_assessment(db_session: Session, assessment: RestBewertungCreate) -> RestBewertungReturn:
    """Add the given assessment to the Database.

    Args:
        db_session (sqlalchemy.orm.Session): Session to the DB -> See `db: Session = Depends(get_db)`
        assessment (schemes.scheme_rest.RestBewertungCreate): The assessment need to be unique

    Raises:
        schemes.exceptions.DatabaseException: if the User or Restaurant does not exist or the assessment is duplicated

    Returns:
        [schemes.scheme_rest.RestBewertungReturn]: The created Restaurant
    """
    try:
        created_assessment = crud_restBewertung.create_bewertung(db_session, assessment)
        return RestBewertungReturn(
            name=created_assessment.restaurant.name,
            email=created_assessment.person_email,
            place_id=created_assessment.place_id,
            comment=created_assessment.kommentar,
            rating=created_assessment.rating,
            timestamp=created_assessment.zeitstempel,
        )
    except DatabaseException as error:
        raise error


def update_assessment(
    db_session: Session, old_assessment: RestBewertungCreate, new_assessment: RestBewertungCreate
) -> RestBewertungReturn:
    """Update the comment and rating of a existing assessment

    Args:
        db_session (sqlalchemy.orm.Session): Session to the DB -> See `db: Session = Depends(get_db)`
        old_assessment (schemes.scheme_rest.RestBewertungCreate): The current assessment
        new_assessment (schemes.scheme_rest.RestBewertungCreate): The new assessment with the updated values

    Raises:
        schemes.exceptions.DatabaseException: if the User or Restaurant does not exist

    Returns:
        schemes.scheme_rest.RestBewertungReturn: Restaurant with the new values
    """
    try:
        updated_assessment = crud_restBewertung.update_bewertung(db_session, old_assessment, new_assessment)
    except DatabaseException as error:
        raise error
    return RestBewertungReturn(
        name=updated_assessment.restaurant.name,
        email=updated_assessment.person_email,
        place_id=updated_assessment.place_id,
        comment=updated_assessment.kommentar,
        rating=updated_assessment.rating,
        timestamp=updated_assessment.zeitstempel,
    )


def delete_assessment(db_session: Session, user: UserBase, rest: RestaurantBase) -> int:
    """Delete one assessment that are mapped between the user and rest

    Args:
        db_session (sqlalchemy.orm.Session): Session to the DB -> See `db: Session = Depends(get_db)`
        user (schemes.scheme_user.UserBase): The owner of the assessment
        rest (schemes.scheme_rest.RestaurantBase): The mapped Restaurant

    Raises:
        schemes.exceptions.DatabaseException: if the User or Restaurant does not exist

    Returns:
        int: The number of affected Rows of the delete
    """
    rows = crud_restBewertung.delete_bewertung(db_session, user, rest)
    if rows == 0:
        raise DatabaseException("Can not delete assessment. Does the user and restaurant excist?")
    return rows


def get_rest_filter_from_user(db_session: Session, user: UserBase) -> Union[FilterRestDatabase, None]:
    """Return the saved Filter from the Database if found one

    Args:
        db_session (sqlalchemy.orm.Session): Session to the Database
        user (schemes.scheme_user.UserBase): Owner of the filter

    Returns:
        Union[schemes.scheme_filter.FilterRest, None]: Return the Filter or None
    """
    db_filter_rest = crud_filter.get_filter_from_user(db_session, user)
    if db_filter_rest:
        filter_rest = FilterRestDatabase.from_orm(db_filter_rest)
        return filter_rest
    return None


def create_rest_filter(db_session: Session, filter_rest: FilterRestDatabase, user: UserBase) -> FilterRestDatabase:
    """Add a Filter to an existing person

    Args:
        db_session (sqlalchemy.orm.Session): Session to the Database
        filter_rest (schemes.scheme_filter.FilterRestDatabase): Filter to add
        user (schemes.scheme_user.UserBase): Owner of the Filter

    Raises:
        schemes.exceptions.UserNotFound: If the User does not exist

    Returns:
        schemes.scheme_filter.FilterRestDatabase: Added Filter
    """
    try:
        db_filter_rest = crud_filter.create_filterRest(db_session, filter_rest, user)
        filter_rest = FilterRestDatabase.from_orm(db_filter_rest)
        return filter_rest
    except (UserNotFound, DuplicateEntry) as error:
        raise error


def update_rest_filter(db_session: Session, filter_updated: FilterRestDatabase, user: UserBase) -> FilterRestDatabase:
    """Update a Filter from a User. Need the full information of the filter (not only the new one)

    Args:
        db_session (sqlalchemy.orm.Session): Session to the Database
        filter_updated (schemes.scheme_filter.FilterRestDatabase): The new Filter for the user
        user (schemes.scheme_user.UserBase): Owner of the Filter

    Raises:
        schemes.exceptions.UserNotFound: If the User is not in the db

    Returns:
        schemes.scheme_filter.FilterRestDatabase: The updated Filter
    """
    try:
        db_filter_rest = crud_filter.update_filterRest(db_session, filter_updated, user)
        filter_rest = FilterRestDatabase.from_orm(db_filter_rest)
        return filter_rest
    except UserNotFound as error:
        raise error


def search_for_restaurant(db_session: Session, user: UserBase, user_f: FilterRest) -> Restaurant:
    """Do a full search for a Restaurant. This does the google search, weights the result with the user rating
    and choose one of the restaurants according to the weights

    Args:
        db_session (sqlalchemy.orm.Session): Session to the DB -> See `db: Session = Depends(get_db)`
        user (schemes.scheme_user.UserBase): User that contain the mail address
        user_f (schemes.scheme_filter.FilterRest): Filter that are needed for the search

    Raises:
        schemes.exceptions.NoResultsException: If no Results are found
        schemes.exceptions.GoogleApiException: If no communication with the Google API are possible

    Returns:
        schemes.scheme_rest.Restaurant: The one choosen Restaurant where the user have to go now!
    """
    google_rests: List[Restaurant] = gapi.search_restaurant(user_f)
    filterd_rests: List[Restaurant] = apply_filter(google_rests, user_f)

    if len(filterd_rests) == 0:
        raise NoResultsException("There are no Restaurants found with these parameters")

    user_rests: List[Restaurant] = fill_user_rating(db_session, filterd_rests, user)
    restaurant = select_restaurant(user_rests)

    try:
        restaurant = gapi.place_details(restaurant)
    except httpx.HTTPError as error:
        raise GoogleApiException("Can't communicate with the Google API") from error

    if not crud_restaurant.get_restaurant_by_id(db_session, restaurant.place_id):
        crud_restaurant.create_restaurant(db_session, restaurant)
    if not crud_restBewertung.get_bewertung_from_user_to_rest(db_session, user, restaurant):
        add_assessment(db_session, RestBewertungCreate(name=restaurant.name, person=user, restaurant=restaurant))
    return restaurant


def fill_user_rating(db_session: Session, rests: List[Restaurant], user: UserBase) -> List[Restaurant]:
    """Search in the connected DB if one restaurant got already rated from the user
    and if so add the value to the restaurant

    Args:
        db_session (sqlalchemy.orm.Session): Session to the DB -> See `db: Session = Depends(get_db)`
        google_res (List[schemes.scheme_rest.Restaurant]): Restaurants for lookup

    Returns:
        List[schemes.scheme_rest.Restaurant]: Return of the input List with the user rating if one got found
    """
    for rest in rests:
        assessment = crud_restBewertung.get_bewertung_from_user_to_rest(db_session, user, rest)
        if assessment is not None:
            rest.own_rating = assessment.rating

    return rests


def apply_filter(rests: List[Restaurant], user_f: FilterRest) -> List[Restaurant]:
    """Apply all filter (current only Rating)

    Args:
        rests (List[schemes.scheme_rest.Restaurant]): List of all Restarants to apply the filter
        filter (schemes.scheme_filter.FilterRest): The Filter with all informations

    Returns:
        List[schemes.scheme_rest.Restaurant]: The filtered List of the restaurants
    """
    return filter_rating(rests, user_f.rating)


def filter_rating(rests: List[Restaurant], rating: int) -> List[Restaurant]:
    """Remove all Restaurants from the list under the given rating

    Args:
        rests (List[schemes.scheme_rest.Restaurant]): List of all Restarants to filter
        rating (int): All under this number got removed

    Returns:
        List[schemes.scheme_rest.Restaurant]: Filtered List based ob the rating
    """
    for res in rests:
        if res.rating < rating:
            rests.remove(res)
    return rests


def select_restaurant(rests: List[Restaurant]) -> Restaurant:
    """Select one restaurant with specific weight. weight = user_rating * 4 + google_rating * 2.
    If None rating found it will be count as 0

    Args:
        user_res (List[schemes.scheme_rest.Restaurant]): The Rating of the Restaurants are optional

    Returns:
        schemes.scheme_rest.Restaurant: The random chooses restaurant
    """
    weights: List[int] = []
    for res in rests:
        if res.own_rating is None:
            res.own_rating = 0
        if res.rating is None:
            res.rating = 0
        weights.append(res.own_rating * 4 + res.rating * 2)

    return random.choices(rests, weights=weights, k=1)[0]
