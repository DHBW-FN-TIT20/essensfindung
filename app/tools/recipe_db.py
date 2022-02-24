"""Connection to the recipes"""
import json
from datetime import timedelta
from pathlib import Path
from typing import Dict

import pandas


class RecipeDB:
    """Uses Panda to manage the Recipe DB

    Warning:
        Use the `recipe_db` from this module and not your own instance of this class

    Args:
        json_path (Path): Path to the recipeitems.json. Defaults to data/recipeitems.json
    """

    def __init__(self, json_path: Path = Path("data/recipeitems.json")):
        data = self.__read_data__(json_path)
        self.pd_frame = self.__convert_rows__(data)

    @staticmethod
    def __read_data__(path: Path) -> Dict:
        data = []

        with open(path, mode="r", encoding="utf-8") as file:
            for line in file:
                data.append(json.loads(line))

        return data

    @staticmethod
    def __convert_rows__(data: Dict) -> pandas.DataFrame:
        pd_frame = pandas.json_normalize(data)
        pd_frame.cookTime = pandas.to_timedelta(pd_frame.cookTime, errors="coerce")
        pd_frame.prepTime = pandas.to_timedelta(pd_frame.prepTime, errors="coerce")
        return pd_frame

    @staticmethod
    def filter_cooktime(user_pd_frame: pandas.DataFrame, total_time: timedelta) -> pandas.DataFrame:
        """Filter the given DataFrame for the whole cooktime (cookTime+prepTime).
        Only return the recipes with less-equal time

        Args:
            user_pd_frame (pandas.DataFrame): DataFrame to filter
            total_time (timedelta): Max cooktime

        Returns:
            pandas.DataFrame: DataFrame of booleans
        """
        return (user_pd_frame.cookTime + user_pd_frame.prepTime) <= total_time

    @staticmethod
    def filter_keyword(user_pd_frame: pandas.DataFrame, keyword: str) -> pandas.DataFrame:
        """Filter the given DataFrame if the keyword is one of the columns `name`, `description` or `recipeInstrucions`

        Args:
            user_pd_frame (pandas.DataFrame): DataFrame to filter
            keyword (str): The keyword to find

        Returns:
            pandas.DataFrame: DataFrame of booleans
        """
        tmp_data = [False for _ in range(user_pd_frame.shape[0])]
        bool_tmp = pandas.core.series.Series(data=tmp_data)

        for label in ["name", "description", "recipeInstructions"]:
            colum: pandas.core.series.Series = user_pd_frame[label]
            bool_tmp |= colum.str.contains(pat=keyword, case=False, na=False, regex=True)

        return bool_tmp


recipe_db = RecipeDB()
