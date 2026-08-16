from fastapi import APIRouter, Depends
from core.audit import record_audit
from core.dependencies import require_login, require_admin
from core.repository import BaseRepository


def crud_router(config):
    repo = BaseRepository(config["collection"])
    router = APIRouter(prefix=config["prefix"], tags=[config["tag"]])
    collection = config["collection"]
    key = config.get("response_key", collection[:-1] if collection.endswith("s") else collection)
    payload_key = config.get("payload_key")
    entity_type = config.get("entity_type", collection.rstrip("s"))
    unwrap = lambda data: data.get(payload_key, data) if payload_key else data
    wrap = lambda data: {"success": True, key: data}

    @router.get("")
    def get_all(user=Depends(require_login)): return {"success": True, collection: repo.get_all()}

    @router.post("")
    def create(data: dict, user=Depends(require_admin)):
        data = unwrap(data)
        result = repo.insert(data)
        record_audit(user["id"], "create", entity_type, result.get("id"), after=result, application_instance_id=result.get("application_instance_id"), metadata={"source": "web"})
        return wrap(result)

    @router.put("/{item_id}")
    def update(item_id: int, data: dict, user=Depends(require_admin)):
        data = unwrap(data)
        before = repo.get(item_id)
        result = repo.update(item_id, data)
        if result:
            record_audit(user["id"], "update", entity_type, item_id, before=before, after=result, application_instance_id=result.get("application_instance_id"), metadata={"source": "web"})
        return wrap(result)

    @router.delete("/{item_id}")
    def delete(item_id: int, user=Depends(require_admin)):
        before = repo.get(item_id)
        result = repo.delete(item_id)
        if result:
            record_audit(user["id"], "delete", entity_type, item_id, before=before, application_instance_id=before.get("application_instance_id") if before else None, metadata={"source": "web"})
        return {"success": True, **({key: result} if key else {})}

    return router
