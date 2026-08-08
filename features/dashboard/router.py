from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.dependencies import require_login


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

templates = Jinja2Templates(
    directory="templates"
)


@router.get(
    "",
    response_class=HTMLResponse
)
def dashboard_page(
    request: Request,
    user=Depends(require_login)
):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user
        }
    )