"""Data access for AuditLog — see docs/07-agents/audit.md.

No business logic here (see docs/09-backend/architecture.md layer rules) —
callers decide *what* to log; this only persists it.
"""
import uuid

from sqlalchemy.orm import Session as DbSession

from app.models.audit_log import AuditLog, AuditOutcome

_RESULT_SUMMARY_MAX_LENGTH = 500


class AuditLogRepository:
    def __init__(self, db: DbSession):
        self._db = db

    def record(
        self,
        *,
        user_id: uuid.UUID | None,
        agent_name: str,
        outcome: AuditOutcome,
        success: bool,
        tool_name: str | None = None,
        permission: str | None = None,
        risk: str | None = None,
        result_summary: str | None = None,
    ) -> AuditLog:
        if result_summary is not None and len(result_summary) > _RESULT_SUMMARY_MAX_LENGTH:
            result_summary = result_summary[: _RESULT_SUMMARY_MAX_LENGTH - 1] + "…"

        entry = AuditLog(
            user_id=user_id,
            agent_name=agent_name,
            tool_name=tool_name,
            permission=permission,
            risk=risk,
            outcome=outcome.value,
            success=success,
            result_summary=result_summary,
        )
        self._db.add(entry)
        self._db.commit()
        self._db.refresh(entry)
        return entry

    def get_by_id(self, audit_id: uuid.UUID) -> AuditLog | None:
        return self._db.query(AuditLog).filter(AuditLog.id == audit_id).one_or_none()

    def list_for_user(self, user_id: uuid.UUID, limit: int = 50) -> list[AuditLog]:
        return (
            self._db.query(AuditLog)
            .filter(AuditLog.user_id == user_id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .all()
        )
