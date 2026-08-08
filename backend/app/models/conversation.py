"""Conversation entity — see docs/06-ai/memory.md and docs/10-data/entities.md.

Gate 4 (Option A) scope only: a conversation belongs to exactly one user and
holds an ordered list of Messages. No cross-conversation memory, no summary,
no distilled facts — that's the `Memory` entity, explicitly deferred (see
docs/06-ai/memory.md "Target scope (post-MVP)").
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    # Bumped whenever a Message is added — lets GET /conversations order by
    # recency without a join/aggregate over messages.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
