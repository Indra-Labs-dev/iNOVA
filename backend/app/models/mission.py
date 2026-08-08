"""Mission entity — MVP slice, see docs/08-modules/mission-system.md:
"a single linear task (e.g. one ResearchAgent call) with a visible plan of
1 step, completion state, and XP award on success." No MissionTask table —
one row per mission is the whole "plan" at this scope.

Execution is synchronous (no queue/scheduler — see docs/PROJECT_STATUS.md
known gaps), so PENDING/RUNNING are never actually persisted at this Gate:
a Mission is only ever written once, already in its final state. The
column still supports all four values so this remains additive, not a
breaking change, once execution becomes asynchronous.
"""
import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MissionStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Mission(Base):
    __tablename__ = "missions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    goal: Mapped[str] = mapped_column(String(2000), nullable=False)
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    # ResearchAgent's own outcome (e.g. "permission_denied", "invalid_tool_call")
    # when status is FAILED — never masked as a generic failure. NULL on success.
    failure_reason: Mapped[str | None] = mapped_column(String(100), nullable=True)

    answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    xp_awarded: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Links back to the underlying ResearchAgent/tool-level audit entry —
    # Mission is a coarser view, not a replacement for that trail.
    audit_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("audit_logs.id", ondelete="SET NULL"), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
