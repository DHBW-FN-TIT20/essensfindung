import json
from pathlib import Path
from typing import Dict

import pandas

from schemes.scheme_filter import FilterRecipe
from schemes.scheme_recipe import Recipe


class RecipeDB:
    def __init__(self, json_path=Path("./data/recipeitems.json")):
        # self.pd_frame = pandas.read_json(json_path, lines=True, typ=pandas.DataFrame, orient="index", encoding="utf-8")
        data = self.__read_data__(json_path)
        self.pd_frame = self.__convert_rows__(data)

    def __read_data__(self, path: Path) -> Dict:
        data = []
        with open(path, mode="r", encoding="utf-8") as file:
            for line in file:
                data.append(json.loads(line))
        return data

    def __convert_rows__(self, data: Dict) -> pandas.DataFrame:
        pd_frame = pandas.json_normalize(data)

        pd_frame.cookTime = pandas.to_timedelta(pd_frame.cookTime, errors="coerce")
        pd_frame.prepTime = pandas.to_timedelta(pd_frame.prepTime, errors="coerce")
        return pd_frame

    def search_recipe(self, recipe_filter: FilterRecipe) -> pandas.DataFrame:
        bool_tmp = (self.pd_frame.cookTime + self.pd_frame.prepTime) <= recipe_filter.totalTime
        return self.pd_frame[bool_tmp]


recipe_db = RecipeDB()
