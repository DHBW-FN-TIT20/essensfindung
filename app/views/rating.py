import fastapi
from fastapi import Depends
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from db.database import get_db
from sqlalchemy.orm import Session
from tools.security import get_current_user
from schemes.scheme_user import User
from services import service_res

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()


@router.get("/rating", response_class=HTMLResponse)
async def rating(
    request: Request,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rest_ratings = service_res.get_assessments_from_user(db_session=db_session, user=current_user)

    return templates.TemplateResponse(
        "rating/rating.html", {"request": request, "rest_ratings":rest_ratings}
    )
