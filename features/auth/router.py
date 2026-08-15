from fastapi import APIRouter, Request
from pydantic import BaseModel
from .service import authenticate_user, register_user


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(
    data: LoginRequest,
    request: Request,
):
    user = authenticate_user(
        data.username,
        data.password,
    )

    if user is None:
        return {
            "success": False,
            "message": "Invalid username or password.",
        }

    request.session["user_id"] = user["id"]
    request.session["username"] = user["username"]
    request.session["role"] = user["role"]

    return {
        "success": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
        }
    }