from fastapi import Request
from fastapi.responses import RedirectResponse


def require_login(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )
    return request.session

def redirect_if_login(request: Request):
    if "user_id" in request.session:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )
    return None

def require_admin(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse(
            "/login",
            status_code=303
        )
    if request.session["role"] != "admin":
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    return request.session