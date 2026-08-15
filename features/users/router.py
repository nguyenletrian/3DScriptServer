from fastapi import APIRouter, Form, Depends

from core.dependencies import require_admin

from .service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
    authenticate_user,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("")
def get_users(
    user=Depends(require_admin)
):

    users = get_all_users()

    return {
        "success": True,
        "users": [
            {
                "id": item["id"],
                "username": item["username"],
                "role": item["role"],
            }
            for item in users
        ],
    }


@router.get("/{user_id}")
def get_user(
    user_id: int,
    user=Depends(require_admin)
):

    result = get_user_by_id(user_id)

    if result is None:
        return {
            "success": False,
            "message": "User not found.",
        }

    return {
        "success": True,
        "user": {
            "id": result["id"],
            "username": result["username"],
            "role": result["role"],
        },
    }


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    user=Depends(require_admin)
):

    result = delete_user(user_id)

    if result is None:
        return {
            "success": False,
            "message": "User not found.",
        }

    return {
        "success": True,
        "message": "User deleted.",
    }