Recipe
======

Service for all Recipe interactions

.. py:method:: services.service_rec.search_recipe(recipe_filter: FilterRecipe) -> Recipe

    Search for a recipe with the given filter
    
    :param recipe_filter: Filter the Recipes
    :type recipe_filter: schemes.scheme_filter.FilterRecipe

    :return: The one choosen Recipe
    :rtype: schemes.scheme_recipe.Recipe