import fastapi
from fastapi import Depends
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from db.database import get_db
from sqlalchemy.orm import Session

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()

@router.get("/rating", response_class=HTMLResponse)
async def rating(
    db_session: Session = Depends(get_db)
):
