"""Router and Logic for the Recipe of the Website"""
from datetime import timedelta
from typing import Union

import fastapi
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from db.database import get_db
from schemes import scheme_cuisine
from schemes import scheme_filter
from schemes.scheme_user import User
from services import service_rec
from tools.security import get_current_user


templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/findrecipe", response_class=HTMLResponse)
async def findrecipe(
    request: Request,
    length: int,
    keywords: Union[str, None] = None,
    db_session: Session = fastapi.Depends(get_db),
    current_user: User = fastapi.Depends(get_current_user),
):
    """Requests user settings and search for recipe.

    Args:
        request (Request): the http request
        length (int): the minimal length
        keywords (Union[str, None], optional): the keywords. Defaults to None.

    Returns:
        TemplateResponse: the http response
    """
    if length == 0:
        total_length = timedelta(days=100)
    else:
        total_length = timedelta(seconds=length)
    rec_filter = scheme_filter.FilterRecipe(
        cuisines=[scheme_cuisine.PydanticCuisine(name="Restaurant")],
        rating=1,
        keyword=keywords,
        total_time=total_length,
    )
    recipe = service_rec.search_recipe(db_session=db_session, user=current_user, recipe_filter=rec_filter)

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

    prep_time = {
        "days": prep_time_days,
        "hours": prep_time_hours,
        "minutes": prep_time_minutes,
        "seconds": prep_time_seconds,
    }
    cook_time = {
        "days": cook_time_days,
        "hours": cook_time_hours,
        "minutes": cook_time_minutes,
        "seconds": cook_time_seconds,
    }

    return templates.TemplateResponse(
        "recipe/recipe_result.html",
        {"request": request, "recipe": recipe, "prepTime": prep_time, "cookTime": cook_time},
    )
