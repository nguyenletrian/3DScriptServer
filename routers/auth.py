from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from dependencies.auth import require_login,redirect_if_login

from services.user_service import (
    authenticate_user,
    create_user,
)


router = APIRouter()

templates = Jinja2Templates(directory="templates")

### REGISTER
@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    response = redirect_if_login(request)
    if response:
        return response    
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )

@router.post("/register", response_class=HTMLResponse)
def register_user(
    request: Request,
    username: str = Form(""),
    password: str = Form("")
):
    result = create_user(
        username=username,
        password=password
    )
    if not result["success"]:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": result["message"],
                "username": username
            }
        )
    return RedirectResponse(
        "/login",
        status_code=303
    )

# LOGIN
@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    response = redirect_if_login(request)
    if response:
        return response
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )

@router.post("/login", response_class=HTMLResponse)
def login_user(
    request: Request,
    username: str = Form(""),
    password: str = Form("")
):
    result = authenticate_user(username, password)
    if not result["success"]:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": result["message"],
                "username": username
            }
        )
    user = result["user"]
    request.session["user_id"] = user["id"]
    request.session["username"] = user["username"]
    request.session["role"] = user["role"]
    return RedirectResponse(
        "/dashboard",
        status_code=303
    )

### DASHBOAR
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request,session = Depends(require_login)):
    response = require_login(request)
    if response:
        return response
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "username": request.session["username"]
        }
    )


### LOGOUT
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(
        "/login",
        status_code=303
    )