from datetime import timedelta

from schemes import Cuisine
from schemes.scheme_cuisine import PydanticCuisine
from schemes.scheme_filter import FilterRecipe
from tools.recipe_db import recipe_db
from tools.recipe_db import RecipeDB


def test_create_dataframe():
    try:
        RecipeDB()
    except Exception:
        assert False, "Can not create Panda_Dataframe"
    else:
        assert True, "Dataframe created"


def test_search_recipe():
    recipe_filter = FilterRecipe(
        cuisines=[PydanticCuisine(name=Cuisine.GERMAN.value)], rating=3, totalTime=timedelta(minutes=10)
    )

    recipe_df = recipe_db.search_recipe(recipe_filter)
