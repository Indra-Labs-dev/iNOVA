"""AuditLog entity — see docs/07-agents/audit.md and docs/12-security/audit-logging.md.

Written for every permissioned action attempt, not just successes (see
docs/07-agents/audit.md "every step in this chain is logged"). `result_summary`
is deliberately bounded and must never carry secrets or unbounded raw content
(see docs/12-security/secrets.md) — callers are responsible for summarizing
before writing, this model only enforces a length ceiling.
"""
import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AuditOutcome(str, enum.Enum):
    SUCCESS = "success"
    PERMISSION_DENIED = "permission_denied"
    INVALID_TOOL_CALL = "invalid_tool_call"
    INVALID_ARGUMENTS = "invalid_arguments"
    CONFIRMATION_REQUIRED = "confirmation_required"
    EXECUTION_FAILED = "execution_failed"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)

    # WHO
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # WHICH AGENT / WHICH TOOL / WHICH PERMISSION
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False)
    tool_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    permission: Mapped[str | None] = mapped_column(String(100), nullable=True)
    risk: Mapped[str | None] = mapped_column(String(10), nullable=True)

    # RESULT / SUCCESS-FAILURE
    outcome: Mapped[str] = mapped_column(String(30), nullable=False)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    result_summary: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # WHEN
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
