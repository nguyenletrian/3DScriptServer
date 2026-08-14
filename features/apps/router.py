from fastapi import APIRouter
from .service import get_apps

router = APIRouter(prefix="/apps",tags=["Apps"])
@router.get("")
def apps():
    return {
        "success": True,
        "apps": get_apps()
    }