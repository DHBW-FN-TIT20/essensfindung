"""Router for the Home of the Website"""
from typing import Union

from datetime import timedelta
import fastapi
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from schemes import scheme_filter
from services import service_rec
from schemes import scheme_cuisine


templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/findrecipe", response_class=HTMLResponse)
async def findrecipe(
    request: Request,
    length: int,
    keywords: Union[str, None] = None,
):
    if length == 0:
        total_length = timedelta(days=100)
    else:
        total_length = timedelta(seconds=length)
    rec_filter = scheme_filter.FilterRecipe(
        cuisines = [scheme_cuisine.PydanticCuisine(name="Restaurant")],
        rating = 1,
        keyword = keywords,
        total_time = total_length,
    )
    recipe = service_rec.search_recipe(recipe_filter=rec_filter)

    prep_time_total_seconds = recipe.prepTime.total_seconds()
    prep_time_days = int(prep_time_total_seconds // 86400)
    prep_time_hours = int((prep_time_total_seconds % 86400) // 3600)
    prep_time_minutes = int((prep_time_total_seconds % 3600) // 60)
    prep_time_seconds = int(prep_time_total_seconds % 60)

    cook_time_total_seconds = recipe.cookTime.total_seconds()
    cook_time_days = int(cook_time_total_seconds // 86400)
    cook_time_minutes = int((cook_time_total_seconds % 86400) // 3600)
    cook_time_hours = int(cook_time_total_seconds // 3600)
    cook_time_minutes = int((cook_time_total_seconds % 3600) // 60)
    cook_time_seconds = int(cook_time_total_seconds % 60)

    prep_time = {"days": prep_time_days, "hours": prep_time_hours, "minutes": prep_time_minutes, "seconds": prep_time_seconds}
    cook_time = {"days": cook_time_days, "hours": cook_time_hours, "minutes": cook_time_minutes, "seconds": cook_time_seconds}

    return templates.TemplateResponse(
        "recipe/recipe_result.html", {"request": request, "recipe": recipe, "prepTime": prep_time, "cookTime": cook_time}
    )
