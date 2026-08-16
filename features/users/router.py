from fastapi import APIRouter, Depends

from core.dependencies import require_admin

from .service import (
    create_user as create_user_service,
    get_all_users,
    get_user_by_id,
    update_user as update_user_service,
    delete_user as delete_user_service,
)


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("")
def get_users(user=Depends(require_admin)):
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
def get_user(user_id: int, user=Depends(require_admin)):
    result = get_user_by_id(user_id)
    if result is None:
        return {"success": False, "message": "User not found."}

    return {
        "success": True,
        "user": {
            "id": result["id"],
            "username": result["username"],
            "role": result["role"],
        },
    }


@router.post("")
def create_user(data: dict, user=Depends(require_admin)):
    result = create_user_service(
        data.get("username", ""),
        data.get("password", ""),
        data.get("role", "user"),
    )

    if not result["success"]:
        return result

    created = result["user"]
    return {
        "success": True,
        "message": result["message"],
        "user": {
            "id": created["id"],
            "username": created["username"],
            "role": created["role"],
        },
    }


@router.put("/{user_id}")
def update_user(user_id: int, data: dict, user=Depends(require_admin)):
    result = update_user_service(
        user_id,
        data.get("username", ""),
        data.get("role", "user"),
    )

    if not result["success"]:
        return result

    updated = result["user"]
    return {
        "success": True,
        "message": result["message"],
        "user": {
            "id": updated["id"],
            "username": updated["username"],
            "role": updated["role"],
        },
    }


@router.delete("/{user_id}")
def delete_user(user_id: int, user=Depends(require_admin)):
    result = delete_user_service(user_id)
    return result
