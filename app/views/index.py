"""Router for the Home of the Website"""
import fastapi
from fastapi import Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from db.database import get_db
from schemes import Allergies
from schemes import Cuisine
from schemes import scheme_cuisine
from schemes import scheme_filter
from schemes.scheme_user import UserLogin
from services import service_res
from tools.security import get_current_user
from tools.legal import read_legal

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/main", response_class=HTMLResponse)
def main(request: Request, current_user: UserLogin = Depends(get_current_user), db_session: Session = Depends(get_db)):
    """Return the renderd template for the /main.html

    Args:
        request (Request): Requerd for Template
        current_user (UserLogin, optional): the current user logged in. Defaults to Depends(get_current_user).
        db_session (Session, optional): the db session. Defaults to Depends(get_db).

    Returns:
        TemplateResponse: the http response
    """

    # request filter of user
    rest_filter_db = service_res.get_rest_filter_from_user(db_session=db_session, user=current_user)

    # default filter for first login
    if rest_filter_db is None:
        cuisine_list = [scheme_cuisine.PydanticCuisine(name=scheme_cuisine.Cuisine.RESTAURANT.value)]
        rest_filter_db = scheme_filter.FilterRestDatabase(
            cuisines=cuisine_list, allergies=None, rating=4, costs=2, radius=5000, manuell_location="Friedrichshafen"
        )
        service_res.create_rest_filter(db_session=db_session, filter_rest=rest_filter_db, user=current_user)

    # rest_filter-cuisine to comma seperated str
    cuisines_selected: str = ",".join([cuisine.name for cuisine in rest_filter_db.cuisines])
    # cuisine_options from Enum to comma seperated str
    cuisines_options: str = ",".join([cuisine.value for cuisine in Cuisine])

    allergies_selected = ""
    if rest_filter_db.allergies is not None:
        allergies_selected: str = ",".join([allergie.name for allergie in rest_filter_db.allergies])

    allergies_options: str = ",".join([allergie.value for allergie in Allergies])
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "rest_filter": rest_filter_db,
            "cuisines_selected": cuisines_selected,
            "cuisines_selected_arr": [cuisine.name for cuisine in rest_filter_db.cuisines],
            "cuisines_options": cuisines_options,
            "cuisines_options_arr": [cuisine.value for cuisine in Cuisine],
            "allergies_selected": allergies_selected,
            "allergies_selected_arr": allergies_selected.split(","),
            "allergies_options": allergies_options,
            "allergies_options_arr": allergies_options.split(","),
            "username": current_user.email,
        },
    )


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db_session: Session = Depends(get_db)):  # <- REMOVE DB WITH MOCKED USER
    """Return landing page for new users

    Args:
        request (Request): the http request
        db_session (Session, optional): the db session. Defaults to Depends(get_db).

    Returns:
        TemplateResponse: the http response
    """

    # TODO: Remove Mocked User ##########
    try:
        from db.crud.user import create_user
        from schemes.scheme_user import UserCreate
        from schemes.exceptions import DuplicateEntry

        create_user(db_session, UserCreate(email="example@gmx.de", password="password"))
    except DuplicateEntry:
        db_session.rollback()

    ############ END REMOVE ###############

    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/impressum", response_class=HTMLResponse)
def impressum(request: Request):
    """Return legal page
    
    Args:
        request (Request): the http request
    
    Returns:
        TemplateResponse: the http response
    """
    return templates.TemplateResponse("impressum.html", {"request": request, "entity": read_legal()})