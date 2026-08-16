from fastapi import APIRouter, Depends
from core.dependencies import require_login, require_admin
from core.repository import BaseRepository


def crud_router(config):
    repo = BaseRepository(config["collection"])
    router = APIRouter(prefix=config["prefix"], tags=[config["tag"]])
    collection = config["collection"]
    key = config.get("response_key", collection[:-1] if collection.endswith("s") else collection)
    payload_key = config.get("payload_key")
    unwrap = lambda data: data.get(payload_key, data) if payload_key else data
    wrap = lambda data: {"success": True, key: data}

    @router.get("")
    def get_all(user=Depends(require_login)): return {"success": True, collection: repo.get_all()}
    @router.post("")
    def create(data: dict, user=Depends(require_admin)): return wrap(repo.insert(unwrap(data)))
    @router.put("/{item_id}")
    def update(item_id: int, data: dict, user=Depends(require_admin)): return wrap(repo.update(item_id, unwrap(data)))
    @router.delete("/{item_id}")
    def delete(item_id: int, user=Depends(require_admin)): return {"success": True, **({key: repo.delete(item_id)} if key else {})}
    return router
