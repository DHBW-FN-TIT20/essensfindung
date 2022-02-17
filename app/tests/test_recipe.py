from datetime import timedelta

import numpy as np
import pandas
import pytest
from pytest_mock import MockerFixture

from schemes.scheme_filter import FilterRecipe
from schemes.scheme_recipe import Recipe
from services import service_rec
from tools.recipe_db import RecipeDB


@pytest.fixture
def recipe_filter() -> FilterRecipe:
    return FilterRecipe(keyword="Rice", total_time=timedelta(minutes=10))


@pytest.fixture
def recipe_db() -> RecipeDB:
    return RecipeDB()


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


def test_search_recipe(mocker: MockerFixture, recipe_filter: FilterRecipe):
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
    recipe_return = service_rec.search_recipe(recipe_filter=recipe_filter)
    assert recipe_return == random_recipe
