from fastapi import APIRouter, Request, Form,Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from services.user_service import (get_all_users,delete_user,get_user_by_id,update_user)
from dependencies.auth import require_admin

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/users", response_class=HTMLResponse)
def users_page(request: Request,session = Depends(require_admin)):
    users = get_all_users()
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={
            "username":session["username"],
            "users": users
        }
    )

@router.get("/users/delete/{user_id}")
def user_delete(user_id: int,session = Depends(require_admin)):
    delete_user(user_id)
    return RedirectResponse("/users",status_code=303)

# EDIT USER
@router.get("/users/edit/{user_id}", response_class=HTMLResponse)
def edit_page(
    request: Request,
    user_id: int,
    session = Depends(require_admin)
):
    user = get_user_by_id(user_id)
    return templates.TemplateResponse(
        request=request,
        name="edit_user.html",
        context={
            "username":session["username"],
            "user": user
        }
    )

@router.post("/users/edit/{user_id}")
def edit_user(
    request: Request,
    user_id: int,
    username: str = Form(...),
    role: str = Form(...),
    session = Depends(require_admin)
):
    update_user(
        user_id,
        username,
        role
    )
    return RedirectResponse(
        "/users",
        status_code=303
    )