from fastapi import APIRouter
from pydantic import BaseModel

from .service import (authenticate_user,register_user,)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest):

    user = authenticate_user(
        data.username,
        data.password
    )

    if user is None:
        return {
            "success": False,
            "message": "Invalid username or password."
        }

    return {
        "success": True,
        "user": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"]
        }
    }

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(data: RegisterRequest):

    user = register_user(
        data.username,
        data.password,
    )

    if user is None:

        return {
            "success": False,
            "message": "Username already exists.",
        }

    return {
        "success": True,
        "message": "Registration successful.",
    }