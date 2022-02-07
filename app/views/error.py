import fastapi
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.templating import Jinja2Templates

templates = Jinja2Templates("templates")
router = fastapi.APIRouter()

@router.get("/error", response_class=HTMLResponse)
def error(request: Request, err_msg: str):
    """Return landing page for errors"""

    return templates.TemplateResponse("shared/failed_search.html", {"request": request, "err_msg": err_msg})
