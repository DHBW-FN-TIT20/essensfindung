import json
from typing import List

import pytest
from db.base_class import Base
from db.crud.user import create_user
from pytest_httpx import HTTPXMock
from pytest_mock import MockerFixture
from schemes import Allergies
from schemes import Cuisine
from schemes.scheme_filter import FilterRest
from schemes.scheme_rest import LocationBase
from schemes.scheme_rest import Restaurant
from schemes.scheme_user import UserCreate
from services import service_res
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.mark.filterwarnings("ignore")
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()


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
    httpx_mock: HTTPXMock,
    db_session: Session,
    rated_restaurants: List[Restaurant],
    google_api_restaurants: List[Restaurant],
    mocker: MockerFixture,
):
    # mocking...
    # ...random
    random_res = rated_restaurants[1]
    mocker.patch("random.choices", return_value=[random_res])

    # ...fill_user_rating currently not function
    mocker.patch("services.service_res.fill_user_rating", return_value=rated_restaurants)

    # ...googleapi
    mocker.patch("tools.gapi.search_restaurant", return_value=google_api_restaurants)
    mocker.patch("tools.config.Setting.GOOGLE_API_KEY", "42")

    url = f"https://maps.googleapis.com/maps/api/place/details/json?key=42&place_id={random_res.place_id}"
    httpx_mock.add_response(status_code=200, json={"result": random_res.dict()}, url=url)

    filter = FilterRest(
        cuisine=Cuisine.DOENER,
        allergies=[Allergies.LACTOSE],
        rating=3,
        costs=3,
        zipcode="88069",
        radius=5000,
        location=LocationBase(lat="1111", lng="345"),
    )

    user = create_user(db_session, UserCreate(email="test@ok.de", password="geheim"))

    return_res = service_res.search_for_restaurant(db_session, user, filter)
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
