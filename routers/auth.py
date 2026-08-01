from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from services.user_service import load_users, save_users


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )


@router.post("/register")
def register_user(
    username: str = Form(...),
    password: str = Form(...)
):
    users = load_users()
    new_user = {
        "id": len(users) + 1,
        "username": username,
        "password": password,
        "role": "user"
    }
    users.append(new_user)
    save_users(users)
    
    return RedirectResponse(
        "/login",
        status_code=303
    )