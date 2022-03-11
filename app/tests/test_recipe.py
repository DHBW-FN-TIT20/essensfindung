from datetime import timedelta

import numpy as np
import pandas
import pytest
from pytest_mock import MockerFixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.base import BewertungRecipe
from db.base_class import Base
from db.crud import user
from schemes.exceptions import RecipeNotFound
from schemes.scheme_filter import FilterRecipe
from schemes.scheme_recipe import Recipe
from schemes.scheme_user import User
from schemes.scheme_user import UserBase
from schemes.scheme_user import UserCreate
from services import service_rec
from tools.recipe_db import RecipeDB

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def recipe_filter() -> FilterRecipe:
    return FilterRecipe(keyword="Rice", total_time=timedelta(minutes=10))


@pytest.fixture
def recipe_db() -> RecipeDB:
    return RecipeDB()


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
def created_user(db_session: SessionTesting):
    db_user = user.create_user(db_session, person=UserCreate(email="test@mail.de", password="geheim"))
    new_user = User.from_orm(db_user)
    return new_user


def test_create_dataframe():
    try:
        RecipeDB()
    except Exception:
        assert False, "Can not create Panda_Dataframe"
    else:
        assert True, "Dataframe created"


def test_filter_cooktime(recipe_db: RecipeDB, recipe_filter: FilterRecipe):
    recipe_df = recipe_db.filter_cooktime(recipe_db.pd_frame, recipe_filter.total_time)
    assert recipe_df is not None


def test_filter_keyword(recipe_db: RecipeDB, recipe_filter: FilterRecipe):
    recipe_df = recipe_db.filter_keyword(recipe_db.pd_frame, recipe_filter.keyword)
    assert recipe_df is not None


def test_search_recipe(
    mocker: MockerFixture, recipe_filter: FilterRecipe, created_user: User, db_session: SessionTesting
):
    random_recipe_df = pandas.DataFrame(
        {
            "_id.$oid": "11123123123",
            "name": "Lecker Fleisch",
            "ingredients": "Alles kochen",
            "url": "https://random.url/",
            "image": np.nan,
            "cookTime": pandas.Timedelta(timedelta(minutes=20)),
            "prepTime": pandas.Timedelta(timedelta(minutes=10)),
        },
        index=[0],
    )

    random_recipe = Recipe(
        id=random_recipe_df["_id.$oid"][0],
        name=random_recipe_df["name"][0],
        ingredients=random_recipe_df["ingredients"][0],
        url=random_recipe_df["url"][0],
        image=random_recipe_df["image"][0],
        cookTime=random_recipe_df["cookTime"][0],
        prepTime=random_recipe_df["prepTime"][0],
    )

    mocker.patch("pandas.DataFrame.sample", return_value=random_recipe_df)
    recipe_return = service_rec.search_recipe(db_session=db_session, user=created_user, recipe_filter=recipe_filter)
    assert recipe_return == random_recipe


def test_search_recipe_cooktime_error(
    mocker: MockerFixture,
    recipe_filter: FilterRecipe,
    recipe_db: RecipeDB,
    created_user: User,
    db_session: SessionTesting,
):
    recipe_filter.total_time = timedelta(seconds=0)
    mocked_return = pandas.core.series.Series(data=[False for _ in range(recipe_db.pd_frame.shape[0])])
    mocker.patch("tools.recipe_db.RecipeDB.filter_cooktime", return_value=mocked_return)

    with pytest.raises(RecipeNotFound):
        service_rec.search_recipe(db_session=db_session, user=created_user, recipe_filter=recipe_filter)


def test_search_recipe_keyword_error(
    mocker: MockerFixture,
    recipe_filter: FilterRecipe,
    recipe_db: RecipeDB,
    created_user: User,
    db_session: SessionTesting,
):
    recipe_filter.keyword = "So etwas steht nicht in der DB"
    mocked_return = pandas.core.series.Series(data=[False for _ in range(recipe_db.pd_frame.shape[0])])
    mocker.patch("tools.recipe_db.RecipeDB.filter_keyword", return_value=mocked_return)

    with pytest.raises(RecipeNotFound):
        service_rec.search_recipe(db_session=db_session, user=created_user, recipe_filter=recipe_filter)
