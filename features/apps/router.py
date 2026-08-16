from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .service import get_apps, create_app
from core.dependencies import require_login

router = APIRouter(prefix="/apps", tags=["Apps"])


class CreateAppRequest(BaseModel):
    name: str


@router.get("")
def apps(user=Depends(require_login)):
    return {"success": True, "apps": get_apps()}


@router.post("")
def create(data: CreateAppRequest, user=Depends(require_login)):
    return {"success": True, "app": create_app(data.name)}