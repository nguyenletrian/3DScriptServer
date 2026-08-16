from fastapi import APIRouter, Depends

from core.dependencies import require_admin
from core.repository import BaseRepository


router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])
repository = BaseRepository("audit_logs")


@router.get("")
def get_audit_logs(application_instance_id: int | None = None, user_id: int | None = None, entity_type: str | None = None, entity_id: int | None = None, user=Depends(require_admin)):
    logs = repository.get_all()
    if application_instance_id is not None: logs = [log for log in logs if log.get("application_instance_id") == application_instance_id]
    if user_id is not None: logs = [log for log in logs if log.get("user_id") == user_id]
    if entity_type is not None: logs = [log for log in logs if log.get("entity_type") == entity_type]
    if entity_id is not None: logs = [log for log in logs if log.get("entity_id") == entity_id]
    return {"success": True, "audit_logs": logs}
