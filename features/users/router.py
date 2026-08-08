from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from core.dependencies import require_admin

from .service import (get_all_users,get_user_by_id,create_user,update_user,delete_user,authenticate_user)

router = APIRouter(prefix="/users",tags=["Users"])

templates = Jinja2Templates(
    directory="templates"
)


@router.get("", response_class=HTMLResponse)
def users_page(
    request: Request,
    user=Depends(require_admin)
):

    users = get_all_users()

    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={
            "username": user["username"],
            "users": users
        }
    )

@router.post("/delete/{user_id}")
def user_delete(
    user_id: int,
    user=Depends(require_admin)
):

    result = delete_user(user_id)

    return RedirectResponse(
        "/users",
        status_code=303
    )

@router.get(
    "/edit/{user_id}",
    response_class=HTMLResponse
)
def edit_page(
    request: Request,
    user_id: int,
    current_user=Depends(require_admin)
):

    user = get_user_by_id(user_id)

    if user is None:
        return RedirectResponse(
            "/users",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="edit_user.html",
        context={
            "username": current_user["username"],
            "user": user
        }
    )

@router.post("/edit/{user_id}")
def edit_user(
    user_id: int,
    username: str = Form(""),
    role: str = Form(""),
    current_user=Depends(require_admin)
):

    result = update_user(
        user_id,
        username,
        role
    )

    return RedirectResponse(
        "/users",
        status_code=303
    )