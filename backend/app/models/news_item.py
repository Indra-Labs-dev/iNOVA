"""NewsItem — one persisted, source-attributed feed entry, see
docs/08-modules/news-intelligence.md.

`title` and `excerpt` are always the source's own RSS text, verbatim —
never AI-generated (see docs/adr/0014-defer-ai-summarization.md: measured
and deferred, not a design preference). `link` is unique — the idempotency
key NewsService upserts on (see docs/08-modules/news-intelligence.md
"Idempotence, not Deduplication" for why this isn't the deferred
semantic-deduplication pipeline stage).
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class NewsItem(Base):
    __tablename__ = "news_items"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    link: Mapped[str] = mapped_column(String(2000), nullable=False, unique=True, index=True)
    excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
