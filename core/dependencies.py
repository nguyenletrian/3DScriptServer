from fastapi import Request, HTTPException


def get_current_user(request: Request):
    user_id = request.session.get("user_id")

    if user_id is None:
        return None

    return {
        "id": user_id,
        "username": request.session.get("username"),
        "role": request.session.get("role")
    }


def require_login(request: Request):
    user = get_current_user(request)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Login required."
        )

    return user


def require_admin(request: Request):
    user = require_login(request)

    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required."
        )

    return user


def redirect_if_login(request: Request):
    return get_current_user(request)