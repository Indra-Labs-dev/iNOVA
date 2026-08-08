"""Source is read-only from the application's perspective — no create/update
method exists on the repository (only the migration seeds rows), so these
tests seed directly via the model, mirroring how the real migration does it.
"""
import uuid

from app.models.source import Source
from app.repositories.source_repository import SourceRepository


def test_list_all_returns_seeded_sources_ordered_by_key(db_session):
    db_session.add_all(
        [
            Source(id=uuid.uuid4(), key="zzz_feed", name="Z Feed", url="https://example.com/z.xml"),
            Source(id=uuid.uuid4(), key="aaa_feed", name="A Feed", url="https://example.com/a.xml"),
        ]
    )
    db_session.commit()

    sources = SourceRepository(db_session).list_all()

    assert [s.key for s in sources] == ["aaa_feed", "zzz_feed"]


def test_list_all_empty_when_no_sources(db_session):
    assert SourceRepository(db_session).list_all() == []
