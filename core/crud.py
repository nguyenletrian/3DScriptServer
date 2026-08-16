from fastapi import APIRouter, Depends, HTTPException
from core.audit import record_audit
from core.dependencies import require_login, require_admin, require_instance_access
from core.repository import BaseRepository


def crud_router(config):
    repo = BaseRepository(config["collection"])
    router = APIRouter(prefix=config["prefix"], tags=[config["tag"]])
    collection = config["collection"]
    key = config.get("response_key", collection[:-1] if collection.endswith("s") else collection)
    payload_key = config.get("payload_key")
    entity_type = config.get("entity_type", collection.rstrip("s"))
    instance_scoped = config.get("instance_scoped", False)
    write_admin_only = config.get("write_admin_only", not instance_scoped)
    unwrap = lambda data: data.get(payload_key, data) if payload_key else data
    wrap = lambda data: {"success": True, key: data}

    def access(user, instance_id, write=False):
        if instance_scoped: require_instance_access(user, instance_id, write=write)
        elif write_admin_only and user.get("role") != "admin": raise HTTPException(403, "Admin access required.")

    def find(item_id, instance_id=None):
        items = repo.get_all()
        return next((x for x in items if str(x.get("id")) == str(item_id) and (not instance_scoped or x.get("application_instance_id") == instance_id)), None)

    @router.get("")
    def get_all(application_instance_id: str = None, user=Depends(require_login)):
        if instance_scoped: access(user, application_instance_id)
        items = repo.get_all()
        if instance_scoped: items = [x for x in items if x.get("application_instance_id") == application_instance_id]
        return {"success": True, collection: items}

    @router.post("")
    def create(data: dict, application_instance_id: str = None, user=Depends(require_login)):
        access(user, application_instance_id, write=True)
        data = unwrap(data)
        if instance_scoped: data["application_instance_id"] = application_instance_id
        result = repo.insert(data)
        record_audit(user["id"], "create", entity_type, result.get("id"), after=result, application_instance_id=application_instance_id, metadata={"source": "web"})
        return wrap(result)

    @router.put("/{item_id}")
    def update(item_id: str, data: dict, application_instance_id: str = None, user=Depends(require_login)):
        access(user, application_instance_id, write=True)
        data = unwrap(data)
        before = find(item_id, application_instance_id)
        if not before: raise HTTPException(404, f"{entity_type} not found.")
        if instance_scoped: data["application_instance_id"] = application_instance_id
        result = repo.update(item_id, data)
        if result: record_audit(user["id"], "update", entity_type, item_id, before=before, after=result, application_instance_id=application_instance_id, metadata={"source": "web"})
        return wrap(result)

    @router.delete("/{item_id}")
    def delete(item_id: str, application_instance_id: str = None, user=Depends(require_login)):
        access(user, application_instance_id, write=True)
        before = find(item_id, application_instance_id)
        if not before: raise HTTPException(404, f"{entity_type} not found.")
        result = repo.delete(item_id)
        if result: record_audit(user["id"], "delete", entity_type, item_id, before=before, application_instance_id=application_instance_id, metadata={"source": "web"})
        return {"success": True, **({key: result} if key else {})}

    return router
