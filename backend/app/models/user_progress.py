"""UserProgress — see docs/10-data/entities.md ("XP, levels, learning
progress") and docs/08-modules/gamification.md.

Deliberately minimal at this Gate: XP only, no `level`/streaks/achievements
— those are explicitly out of scope for Mission System MVP (see
docs/16-roadmap/mvp.md "Explicitly excluded"). Kept as its own table, not a
column on `User`, because identity and progress are different concerns
(see docs/10-data/data-architecture.md: prefer normalized domain models
over one giant "user data" table) — and because `UserProgress` was already
the documented entity name before this Gate, not invented for it.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    xp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
