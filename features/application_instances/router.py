from importlib import import_module
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from core.dependencies import require_login
from core.repository import BaseRepository
from core.audit import record_audit

router = APIRouter(prefix="/application-instances", tags=["Application Instances"])
instances = BaseRepository("application_instances")
permissions = BaseRepository("application_instance_permissions")
applications = BaseRepository("applications")


def seed_application(application_id, instance_id):
    application = applications.get(application_id)
    if not application:
        raise HTTPException(404, "Application not found")
    try:
        module = import_module(f"features.{application.get('short_name', application_id)}.instance")
    except ModuleNotFoundError as error:
        if error.name != f"features.{application.get('short_name', application_id)}.instance": raise
        return
    seed = getattr(module, "seed_instance", None)
    if seed: seed(instance_id)


@router.get("")
def get_instances(user=Depends(require_login)):
    items = [x for x in instances.get_all() if x.get("owner_user_id") == user["id"]]
    return {"success": True, "application_instances": items}


@router.post("/activate")
def activate(data: dict, user=Depends(require_login)):
    application_id = data.get("application_id")
    if application_id is None: raise HTTPException(400, "application_id is required")
    application = applications.get(application_id)
    if not application: raise HTTPException(404, "Application not found")
    existing = next((x for x in instances.get_all() if str(x.get("application_id")) == str(application_id) and x.get("owner_user_id") == user["id"] and x.get("status") == "active"), None)
    if existing:
        seed_application(application_id, existing["id"])
        return {"success": True, "application_instance": existing, "already_active": True}
    instance = {
        "id": f"inst_{uuid4().hex[:10]}", "application_id": application_id, "owner_user_id": user["id"],
        "name": data.get("name") or application.get("name") or application.get("short_name") or str(application_id),
        "address": data.get("address", ""), "phone": data.get("phone", ""), "email": data.get("email", ""),
        "status": "active", "settings": {},
    }
    result = instances.insert(instance)
    application_short_name = application.get("short_name") or application.get("name") or str(application_id)
    result["short_name"] = f"{application_short_name}_{result['id']}"
    instances.update(result["id"], result)
    permissions.insert({
        "id": f"perm_{uuid4().hex[:10]}", "application_instance_id": result["id"], "user_id": user["id"],
        "role": "owner", "permissions": ["*"], "status": "active",
    })
    seed_application(application_id, result["id"])
    record_audit(user["id"], "activate", "application_instance", result["id"], after=result, application_instance_id=result["id"], metadata={"source": "web"})
    return {"success": True, "application_instance": result, "already_active": False}
