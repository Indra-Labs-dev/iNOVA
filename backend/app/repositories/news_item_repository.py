"""Data access for NewsItem — see docs/08-modules/news-intelligence.md.

`get_by_link` + `create` compose the idempotent-by-URL upsert NewsService
performs — see that service for the actual "skip if already present"
decision; this repository only exposes the two primitives.
"""
import uuid
from datetime import datetime

from sqlalchemy.orm import Session as DbSession

from app.models.news_item import NewsItem


class NewsItemRepository:
    def __init__(self, db: DbSession):
        self._db = db

    def get_by_link(self, link: str) -> NewsItem | None:
        return self._db.query(NewsItem).filter(NewsItem.link == link).one_or_none()

    def create(
        self,
        *,
        source_id: uuid.UUID,
        title: str,
        link: str,
        excerpt: str | None,
        published_at: datetime | None,
    ) -> NewsItem:
        item = NewsItem(
            source_id=source_id, title=title, link=link, excerpt=excerpt, published_at=published_at
        )
        self._db.add(item)
        self._db.commit()
        self._db.refresh(item)
        return item

    def list_recent(self, limit: int = 50) -> list[NewsItem]:
        return (
            self._db.query(NewsItem)
            .order_by(NewsItem.published_at.desc().nulls_last(), NewsItem.fetched_at.desc())
            .limit(limit)
            .all()
        )
