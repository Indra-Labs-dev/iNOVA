"""Data access for Source — see docs/08-modules/news-intelligence.md.

Read-only by design: no `create`/`update`/`delete` here. Sources are
seeded exclusively by a migration (see migrations/versions) — this
repository exists so NewsService can list them, nothing more.
"""
from sqlalchemy.orm import Session as DbSession

from app.models.source import Source


class SourceRepository:
    def __init__(self, db: DbSession):
        self._db = db

    def list_all(self) -> list[Source]:
        return self._db.query(Source).order_by(Source.key).all()
