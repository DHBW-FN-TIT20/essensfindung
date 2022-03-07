import json
from typing import List

import pytest
from pytest_httpx import HTTPXMock
from pytest_mock import MockerFixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import db
from db.base_class import Base
from db.crud.allergies import create_allergie
from db.crud.cuisine import create_cuisine
from db.crud.user import create_user
from schemes import Allergies
from schemes import Cuisine
from schemes import scheme_allergie
from schemes import scheme_cuisine
from schemes.scheme_allergie import PydanticAllergies
from schemes.scheme_cuisine import PydanticCuisine
from schemes.scheme_filter import FilterRest
from schemes.scheme_filter import FilterRestDatabase
from schemes.scheme_rest import LocationBase
from schemes.scheme_rest import Restaurant
from schemes.scheme_user import User
from schemes.scheme_user import UserBase
from schemes.scheme_user import UserCreate
from services import service_res

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


@pytest.fixture(scope="function")
def add_allergies(db_session: SessionTesting) -> None:
    for allergie in Allergies:
        create_allergie(db_session, allergie)


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


@pytest.fixture(scope="function")
def add_cuisines(db_session: SessionTesting) -> None:
    for cuisine in Cuisine:
        create_cuisine(db_session, cuisine)


def test_get_rest_filter_from_user(db_session: SessionTesting, add_allergies, mocker: MockerFixture):
    allergies = [db.base.Allergie(name=Allergies.LACTOSE.value), db.base.Allergie(name=Allergies.WHEAT.value)]
    cuisines = [PydanticCuisine(name=Cuisine.GERMAN.value), PydanticCuisine(name=Cuisine.DOENER.value)]
    db_filter = db.base.FilterRest(
        email="test@nice.de", zipcode="88069", radius=5000, rating=3, cuisines=cuisines, costs=3, allergies=allergies
    )

    db_filter_copy = db.base.FilterRest(
        email="test@nice.de", zipcode="88069", radius=5000, rating=3, cuisines=cuisines, costs=3, allergies=allergies
    )

    mocker.patch("db.crud.filter.get_filter_from_user", return_value=db_filter)

    scheme_filter_rest = FilterRestDatabase.from_orm(db_filter_copy)
    assert scheme_filter_rest == service_res.get_rest_filter_from_user(db_session, UserBase(email="test@nice.de"))


def test_create_rest_filter(db_session: SessionTesting, add_allergies, add_cuisines):
    allergies = [db.base.Allergie(name=Allergies.WHEAT.value), db.base.Allergie(name=Allergies.LACTOSE.value)]
    cuisines = [PydanticCuisine(name=Cuisine.GERMAN.value), PydanticCuisine(name=Cuisine.DOENER.value)]
    db_user = create_user(db_session, UserCreate(email="nice@ok.test", password="geheim"))
    user = User.from_orm(db_user)

    db_filter = db.base.FilterRest(
        email="test@nice.de", zipcode="88069", radius=5000, rating=3, cuisines=cuisines, costs=3, allergies=allergies
    )

    scheme_filter_rest = FilterRestDatabase.from_orm(db_filter)
    created_rest = service_res.create_rest_filter(db_session, scheme_filter_rest, user)

    assert scheme_filter_rest == created_rest


def test_update_rest_filter(db_session: SessionTesting, add_allergies, add_cuisines):
    allergies = [db.base.Allergie(name=Allergies.LACTOSE.value), db.base.Allergie(name=Allergies.WHEAT.value)]
    cuisines = [PydanticCuisine(name=Cuisine.GERMAN.value), PydanticCuisine(name=Cuisine.DOENER.value)]
    db_user = create_user(db_session, UserCreate(email="nice@ok.test", password="geheim"))
    user = User.from_orm(db_user)

    db_filter = db.base.FilterRest(
        email="test@nice.de", zipcode="88069", radius=5000, rating=3, cuisines=cuisines, costs=3, allergies=allergies
    )
    scheme_filter_rest = FilterRestDatabase.from_orm(db_filter)
    service_res.create_rest_filter(db_session, scheme_filter_rest, user)

    updated_scheme_filter_rest = scheme_filter_rest.copy()
    updated_scheme_filter_rest.costs = 1
    updated_scheme_filter_rest.allergies = [PydanticAllergies(name=Allergies.LACTOSE.value)]

    assert updated_scheme_filter_rest == service_res.update_rest_filter(db_session, updated_scheme_filter_rest, user)


def test_search_for_restaurant(
    httpx_mock: HTTPXMock,
    db_session: SessionTesting,
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
        cuisines=[scheme_cuisine.PydanticCuisine(name=Cuisine.DOENER.value)],
        allergies=[scheme_allergie.PydanticAllergies(name=Allergies.LACTOSE.value)],
        rating=3,
        costs=3,
        zipcode="88069",
        radius=5000,
        location=LocationBase(lat="1111", lng="345"),
    )

    user = UserCreate(email="test@ok.de", password="geheim")
    create_user(db_session, user)

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
