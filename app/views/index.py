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
from schemes.scheme_user import UserBase
from services import service_res

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/main", response_class=HTMLResponse)
def main(request: Request, db_session: Session = Depends(get_db)):
    """Return the renderd template for the /main.html

    Args:
        request (Request): Requerd for Template
    """

    # TODO: Remove Mocked User
    try:
        from db.crud.user import create_user
        from schemes.scheme_user import UserCreate
        from schemes.exceptions import DuplicateEntry

        create_user(db_session, UserCreate(email="example@gmx.de", password="password"))
    except DuplicateEntry:
        db_session.rollback()

    # request filter of user
    mock_user = UserBase(email="example@gmx.de")
    rest_filter_db = service_res.get_rest_filter_from_user(db_session=db_session, user=mock_user)

    # default filter for first login
    if rest_filter_db is None:
        cuisine_list = [scheme_cuisine.PydanticCuisine(name=scheme_cuisine.Cuisine.DOENER.value)]
        rest_filter_db = scheme_filter.FilterRestDatabase(
            cuisines=cuisine_list, allergies=None, rating=4, costs=2, radius=5000, zipcode="88045"
        )
        service_res.create_rest_filter(db_session=db_session, filter_rest=rest_filter_db, user=mock_user)

    # rest_filter-cuisine to comma seperated str
    cuisines_selected: str = ",".join([cuisine.name for cuisine in rest_filter_db.cuisines])
    # cuisine_options from Enum to comma seperated str
    cuisines_options: str = ",".join([cuisine.value for cuisine in Cuisine])

    allergies_selected = None
    if rest_filter_db.allergies is not None:
        allergies_selected: str = ",".join([allergie.name for allergie in rest_filter_db.allergies])

    allergies_options: str = ",".join([allergie.value for allergie in Allergies])
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "rest_filter": rest_filter_db,
            "cuisines_selected": cuisines_selected,
            "cuisines_options": cuisines_options,
            "allergies_selected": allergies_selected,
            "allergies_options": allergies_options,
            "username": mock_user.email,
        },
    )


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Return landing page for new users"""

    return templates.TemplateResponse("index.html", {"request": request})
