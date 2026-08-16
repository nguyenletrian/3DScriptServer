from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .service import get_apps, create_app, delete_app,update_app
from core.dependencies import require_login, require_admin


router = APIRouter(prefix="/apps", tags=["Apps"])


class AppRequest(BaseModel):
    data: dict


@router.get("")
def apps(user=Depends(require_login)):
    return {"success": True, "apps": get_apps()}


@router.post("")
def create(data: AppRequest, user=Depends(require_admin)):
    return {"success": True, "app": create_app(data.data)}


@router.delete("/{app_id}")
def delete(app_id: int, user=Depends(require_admin)):
    return {"success": True, "app": delete_app(app_id)}

@router.put("/{app_id}")
def update(app_id: int, data: AppRequest, user=Depends(require_admin)):
    return {"success": True, "app": update_app(app_id, data.data)}