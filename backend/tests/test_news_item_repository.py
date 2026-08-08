import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app.models.source import Source
from app.repositories.news_item_repository import NewsItemRepository


def _source(db_session, key="python_blog"):
    source = Source(id=uuid.uuid4(), key=key, name="Python Insider", url="https://example.com/feed.xml")
    db_session.add(source)
    db_session.commit()
    return source


def test_create_news_item(db_session):
    source = _source(db_session)
    repo = NewsItemRepository(db_session)

    item = repo.create(
        source_id=source.id,
        title="Python 3.14.7 released",
        link="https://blog.python.org/2026/08/python-3147.html",
        excerpt="A pair of bug fix releases await your upgrade.",
        published_at=datetime.now(timezone.utc),
    )

    assert item.id is not None
    assert item.title == "Python 3.14.7 released"
    assert item.source_id == source.id


def test_get_by_link_returns_none_when_absent(db_session):
    assert NewsItemRepository(db_session).get_by_link("https://example.com/nope") is None


def test_get_by_link_finds_existing_item(db_session):
    source = _source(db_session)
    repo = NewsItemRepository(db_session)
    repo.create(
        source_id=source.id,
        title="A title",
        link="https://example.com/a",
        excerpt=None,
        published_at=None,
    )

    found = repo.get_by_link("https://example.com/a")

    assert found is not None
    assert found.title == "A title"


def test_link_is_unique(db_session):
    source = _source(db_session)
    repo = NewsItemRepository(db_session)
    repo.create(source_id=source.id, title="First", link="https://example.com/dup", excerpt=None, published_at=None)

    with pytest.raises(Exception):
        repo.create(
            source_id=source.id, title="Second", link="https://example.com/dup", excerpt=None, published_at=None
        )


def test_list_recent_orders_by_published_at_desc(db_session):
    source = _source(db_session)
    repo = NewsItemRepository(db_session)
    now = datetime.now(timezone.utc)
    repo.create(source_id=source.id, title="Older", link="https://example.com/1", excerpt=None, published_at=now - timedelta(days=2))
    repo.create(source_id=source.id, title="Newer", link="https://example.com/2", excerpt=None, published_at=now)

    items = repo.list_recent()

    assert [i.title for i in items] == ["Newer", "Older"]


def test_list_recent_puts_items_without_published_at_last(db_session):
    source = _source(db_session)
    repo = NewsItemRepository(db_session)
    now = datetime.now(timezone.utc)
    repo.create(source_id=source.id, title="No date", link="https://example.com/nodate", excerpt=None, published_at=None)
    repo.create(source_id=source.id, title="Dated", link="https://example.com/dated", excerpt=None, published_at=now)

    items = repo.list_recent()

    assert [i.title for i in items] == ["Dated", "No date"]
