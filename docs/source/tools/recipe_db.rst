Recipe Database
===============

.. hint:: Use `recipe_db <#recipe_db>`_ to interact with the Database if you want

.. py:data:: recipe_db
    :type: tools.recipe_db.RecipeDB

    This contain a loaded class from `RecipeDB <#tools.recipe_db.RecipeDB>`_ 
    Use this to reduce loading time


.. py:class:: tools.recipe_db.RecipeDB(json_path)

    Class to interact with the :file:`data/recipeitems.json` and filter the data

    .. py:staticmethod:: filter_cooktime(user_pd_frame: pandas.DataFrame, total_time: timedelta)

        Filter the given DataFrame for the whole cooktime (cookTime+prepTime).
        Only return the recipes with less-equal time

        :param user_pd_frame: DataFrame to filter
        :type user_pd_frame: pandas.DataFrame
        :param total_time: Max cooktime
        :type total_time: datetime.timedelta
        :return: DataFrame of booleans
        :rtype: pandas.DataFrame

    .. py:staticmethod:: filter_keyword(user_pd_frame: pandas.DataFrame, keyword: str)
    
        Filter the given DataFrame if the keyword is one of the columns `name`, `description` or `recipeInstrucions`

        :param user_pd_frame: DataFrame to filter
        :type user_pd_frame: pandas.DataFrame
        :param keyword: The keyword to find
        :type keyword: str
        :return: DataFrame of booleans
        :rtype: pandas.DataFrame
