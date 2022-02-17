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

    # TODO: Rezept suchen/auswählen

    return templates.TemplateResponse(
        "recipe/recipe_result.html", {"request": request, "recipe": recipe}
    )
