import json
from typing import List
import pytest
from models import Allergies, Cuisine
from services import service_res
from models.restaurant import BaseLocation, Restaurant
from models.filter import RestFilter
from pytest_mock import MockerFixture


@pytest.fixture
def rated_restaurants() -> List[Restaurant]:
    with open("tests/example_restaurants_with_own_rating.json", "r", encoding="utf8") as file:
        fake_restaurants = json.load(file)
        return [Restaurant(**value) for value in fake_restaurants]


@pytest.fixture
def google_api_restaurants() -> List[Restaurant]:
    with open("tests/example_restaurants.json", "r", encoding="utf8") as file:
        fake_restaurants = json.load(file)
        return [Restaurant(**value) for value in fake_restaurants]


def test_search_for_restaurant(
    rated_restaurants: List[Restaurant], google_api_restaurants: List[Restaurant], mocker: MockerFixture
):
    # mocking...
    # ...random
    random_res = rated_restaurants[1]
    mocker.patch("random.choices", return_value=[random_res])

    # ...fill_user_rating currently not function
    mocker.patch("services.service_res.fill_user_rating", return_value=rated_restaurants)

    # ...googleapi
    mocker.patch("infrastructure.gapi.search_restaurant", return_value=google_api_restaurants)

    filter = RestFilter(
        cuisine=Cuisine.DOENER,
        allergies=Allergies.LACTOSE,
        rating=3,
        costs=3,
        location=BaseLocation(lat=42, lng=42),
        radius=5000,
    )
    return_res = service_res.search_for_restaurant(filter)
    assert return_res == random_res


def test_fill_user_rating():
    pass


def test_select_restaurant(rated_restaurants: List[Restaurant], mocker: MockerFixture):
    # mock random
    random_res = rated_restaurants[1]
    mocker.patch("random.choices", return_value=[random_res])

    # Does it return 1 restuarant
    return_res = service_res.select_restaurant(rated_restaurants)
    assert return_res == random_res

    # No error when rating = 0
    rated_restaurants[5].own_rating = 0
    rated_restaurants[7].rating = 0

    return_res = service_res.select_restaurant(rated_restaurants)
    assert return_res == random_res

    # No error when rating = None
    rated_restaurants[5].own_rating = None
    rated_restaurants[7].rating = None

    return_res = service_res.select_restaurant(rated_restaurants)
    assert return_res == random_res
