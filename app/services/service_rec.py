import pandas

from schemes.exceptions import RecipeNotFound
from schemes.scheme_filter import FilterRecipe
from schemes.scheme_recipe import Recipe
from tools.recipe_db import recipe_db
from tools.recipe_db import RecipeDB


def search_recipe(recipe_filter: FilterRecipe) -> Recipe:
    """Search for a recipe with the given filter

    Args:
        recipe_filter (FilterRecipe): Filter the Recipes

    Returns:
        Recipe: The one choosen Recipe
    """
    random_recipe: pandas.DataFrame = __apply_filter(recipe_db.pd_frame, recipe_filter).sample()

    return Recipe(
        id=random_recipe["_id.$oid"][0],
        name=random_recipe["name"][0],
        ingredients=random_recipe["ingredients"][0],
        url=random_recipe["url"][0],
        image=random_recipe["image"][0],
        cookTime=random_recipe["cookTime"][0],
        prepTime=random_recipe["prepTime"][0],
    )


def __apply_filter(recipes: pandas.DataFrame, recipe_filter: FilterRecipe) -> pandas.DataFrame:
    cooktime_bool = RecipeDB.filter_cooktime(user_pd_frame=recipes, total_time=recipe_filter.total_time)
    keyword_bool = RecipeDB.filter_keyword(user_pd_frame=recipes, keyword=recipe_filter.keyword)
    filter_bool = cooktime_bool & keyword_bool

    if not True in filter_bool.value_counts():
        raise RecipeNotFound("No Recipe Found with these Filters")

    return recipes[filter_bool]
