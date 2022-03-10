"""Router and logic for the restaurant of the Website"""
from typing import Union

import fastapi
from fastapi import Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from db.database import get_db
from schemes import scheme_allergie
from schemes import scheme_cuisine
from schemes import scheme_filter
from schemes import scheme_rest
from schemes.scheme_user import User
from services import service_res
from tools.security import get_current_user


templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/findrestaurant", response_class=HTMLResponse)
async def findrestaurant(
    request: Request,
    rating: int,
    costs: float,
    radius: int,
    lat: str,
    lng: str,
    manuell_location: str,
    cuisine: Union[str, None] = None,
    allergies: Union[str, None] = None,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Requests user settings and search for restaurant.

    Args:
        request (Request): the http request
        rating (int): the minimal rating
        costs (float): the minimal costs
        radius (int): the radius
        lat (str): the latitude
        lng (str): the longitude
        manuell_location(str): manuell location for the search
        cuisine (Union[str, None], optional): the selected cuisines. Defaults to None.
        allergies (Union[str, None], optional): the selected allergies. Defaults to None.
        db_session (Session, optional): the db session. Defaults to Depends(get_db).
        current_user (User, optional): the current user. Defaults to Depends(get_current_user).

    Returns:
        RedirectResponse: redirect to /error...
        TemplateResponse: the http response
    """

    if lat == "" or lng == "":
        location = service_res.get_coordinates_from_location(manuell_location)
    else:
        location = scheme_rest.LocationBase(lat=lat, lng=lng)

    # cuisine:str zum Cuisine-Array machen
    if cuisine is not None:
        cuisine_list = [scheme_cuisine.PydanticCuisine(name=cuisine) for cuisine in cuisine.split(",")]
    else:
        cuisine_list = [scheme_cuisine.PydanticCuisine(name="Restaurant")]
    allergies_list = allergies
    if allergies is not None:
        allergies_list = [scheme_allergie.PydanticAllergies(name=allergie) for allergie in allergies.split(",")]
    rest_filter = scheme_filter.FilterRest(
        cuisines=cuisine_list,
        allergies=allergies_list,
        rating=rating,
        costs=costs,
        radius=radius * 1000,
        location=location,
    )
    rest_filter_db = scheme_filter.FilterRestDatabase(
        cuisines=rest_filter.cuisines,
        allergies=rest_filter.allergies,
        rating=rest_filter.rating,
        costs=rest_filter.costs,
        radius=rest_filter.radius,
        manuell_location=manuell_location,
    )
    service_res.update_rest_filter(db_session=db_session, filter_updated=rest_filter_db, user=current_user)
    restaurant = service_res.search_for_restaurant(db_session=db_session, user=current_user, user_f=rest_filter)
    return templates.TemplateResponse(
        "restaurant/restaurant_result.html", {"request": request, "restaurant": restaurant}
    )
