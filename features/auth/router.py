from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from core.dependencies import redirect_if_login,require_login
from .service import authenticate_user, register_user



router = APIRouter(
    tags=["Auth"]
)

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/login", response_class=HTMLResponse)
def login_page(
    request: Request,
    user=Depends(redirect_if_login)
):
    if user is not None:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(""),
    password: str = Form("")
):
    user = authenticate_user(
        username,
        password
    )

    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Invalid username or password.",
                "username": username
            },
            status_code=401
        )

    request.session["user_id"] = user["id"]
    request.session["username"] = user["username"]
    request.session["role"] = user["role"]

    return RedirectResponse(
        "/dashboard",
        status_code=303
    )


@router.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(
    request: Request,
    _=Depends(redirect_if_login)
):
    return templates.TemplateResponse(
        request=request,
        name="register.html"
    )


@router.post("/register")
def register(
    request: Request,
    username: str = Form(""),
    password: str = Form("")
):
    if not username or not password:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "Username and password are required.",
                "username": username
            },
            status_code=400
        )

    user = register_user(
        username,
        password
    )

    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "Username already exists.",
                "username": username
            },
            status_code=400
        )

    return RedirectResponse(
        "/login",
        status_code=303
    )



@router.get("/logout")
def logout(request: Request):
    request.session.clear()

    return RedirectResponse(
        "/login",
        status_code=303
    )

