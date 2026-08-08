"""Source — a server-configured news feed, see docs/08-modules/news-intelligence.md.

Never client-editable: no API surface creates, modifies, or deletes a
Source (same "code change + review" posture as
app/tools/research_tools.py's RSS_ALLOWLIST — that allowlist is in fact
this Gate's seed data, see migrations/versions for the seeding). `key` and
`url` are only ever set by a migration, never by request input.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    url: Mapped[str] = mapped_column(String(2000), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
