import json
from typing import List

import httpx
import pytest
from pytest_httpx import HTTPXMock
from pytest_mock import MockerFixture

from schemes import Cuisine
from schemes.scheme_rest import Restaurant
from tools import gapi


@pytest.fixture
def fake_nearby_search() -> dict:
    with open("tests/example_nearby_search.json", "r", encoding="utf8") as file:
        return json.load(file)


@pytest.fixture
def fake_nearby_search_restaurants(fake_nearby_search: str) -> List[Restaurant]:
    return [Restaurant(**value) for value in fake_nearby_search.get("results")]


@pytest.fixture
def fake_place_details() -> dict:
    with open("tests/example_place_details.json", "r", encoding="utf8") as file:
        return json.load(file)


@pytest.fixture
def fake_restaurants() -> List[Restaurant]:
    with open("tests/example_restaurants.json", "r", encoding="utf8") as file:
        fake_restaurants = json.load(file)
        return [Restaurant(**value) for value in fake_restaurants]


@pytest.mark.parametrize("status_code", [100, 200, 300, 400])
def test_nearby_search(
    mocker: MockerFixture,
    httpx_mock: HTTPXMock,
    status_code: int,
    fake_nearby_search: dict,
    fake_nearby_search_restaurants: List[Restaurant],
):
    # Fake Datas
    params: dict = {
        "keyword": Cuisine.DOENER.value,
        "location": "42,42",
        "opennow": True,
        "radius": "42",
        "type": "restaurant",
        "language": "de",
    }
    # Mock httpx responses
    httpx_mock.add_response(status_code=status_code, json=fake_nearby_search)

    # Mock other functions
    mocker.patch("configuration.config.get_google_api_key", return_value="42")

    if status_code != 200:
        with pytest.raises(httpx.HTTPStatusError):
            gapi.nearby_search(params)
    else:
        restaurants = gapi.nearby_search(params)
        assert fake_nearby_search_restaurants == restaurants


def test_place_details(
    httpx_mock: HTTPXMock,
    fake_place_details: dict,
    fake_restaurants: List[Restaurant],
    fake_nearby_search_restaurants: List[Restaurant],
    mocker: MockerFixture,
):

    # Mock httpx responses
    for fake_place_detail in fake_place_details:
        url = f"https://maps.googleapis.com/maps/api/place/details/json?key=42&place_id={fake_place_detail['result']['place_id']}"
        httpx_mock.add_response(status_code=200, json=fake_place_detail, url=url)

    # Mock other functions
    mocker.patch("configuration.config.get_google_api_key", return_value="42")

    restaurants = gapi.place_details(fake_nearby_search_restaurants)
    assert fake_restaurants == restaurants
