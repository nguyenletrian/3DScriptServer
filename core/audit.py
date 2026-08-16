from datetime import datetime, timezone

from core.repository import BaseRepository


_audit_repository = BaseRepository("audit_logs")


def _changes(before, after):
    before = before or {}
    after = after or {}
    return {
        key: {"from": before.get(key), "to": after.get(key)}
        for key in set(before) | set(after)
        if before.get(key) != after.get(key) and key != "id"
    }


def record_audit(user_id, action, entity_type, entity_id=None, before=None, after=None, application_instance_id=None, metadata=None):
    return _audit_repository.insert({
        "user_id": user_id,
        "application_instance_id": application_instance_id,
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "changes": _changes(before, after) if action == "update" else (after or before or {}),
        "metadata": metadata or {},
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
