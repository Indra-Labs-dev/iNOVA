"""NewsService tests — respx-mocked HTTP, no real network, mirrors
tests/test_llm_provider.py's approach. Covers normalization, idempotent
persistence, per-source failure isolation, and the structural "no AI
call" guarantee.
"""
import uuid

import httpx
import respx

from app.models.source import Source
from app.repositories.news_item_repository import NewsItemRepository
from app.repositories.source_repository import SourceRepository
from app.services.news_service import NewsService

PYTHON_BLOG_XML = b"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>Python Insider</title>
<item>
<title>Python 3.14.7 and 3.13.15 are now available!</title>
<link>https://blog.python.org/2026/08/python-3147-31315/</link>
<description>A pair of bug fix releases await your upgrade.</description>
<pubDate>Wed, 05 Aug 2026 00:00:00 GMT</pubDate>
</item>
<item>
<title>Python 3.15.0 candidate 1 is here!</title>
<link>https://blog.python.org/2026/08/python-3150-rc1/</link>
<description>Get those wheels rolling!</description>
<pubDate>Tue, 04 Aug 2026 00:00:00 GMT</pubDate>
</item>
</channel></rss>"""

GITHUB_BLOG_XML = b"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>The GitHub Blog</title>
<item>
<title>A guide to slash commands</title>
<link>https://github.blog/a-guide/</link>
<description><![CDATA[<p>Go beyond chat with these <b>slash commands</b>.</p>]]></description>
<pubDate>Thu, 06 Aug 2026 19:49:34 +0000</pubDate>
</item>
</channel></rss>"""


def _sources(db_session):
    python_blog = Source(
        id=uuid.uuid4(), key="python_blog", name="Python Insider", url="https://blog.python.org/feed"
    )
    github_blog = Source(
        id=uuid.uuid4(), key="github_blog", name="The GitHub Blog", url="https://github.blog/feed/"
    )
    db_session.add_all([python_blog, github_blog])
    db_session.commit()
    return python_blog, github_blog


def _service(db_session) -> NewsService:
    return NewsService(SourceRepository(db_session), NewsItemRepository(db_session))


@respx.mock
def test_refresh_persists_normalized_items_from_all_sources(db_session):
    python_blog, github_blog = _sources(db_session)
    respx.get(python_blog.url).mock(return_value=httpx.Response(200, content=PYTHON_BLOG_XML))
    respx.get(github_blog.url).mock(return_value=httpx.Response(200, content=GITHUB_BLOG_XML))

    summary = _service(db_session).refresh()

    assert summary.items_new_total == 3
    items = NewsItemRepository(db_session).list_recent()
    assert len(items) == 3
    titles = {i.title for i in items}
    assert "Python 3.14.7 and 3.13.15 are now available!" in titles
    assert "A guide to slash commands" in titles


@respx.mock
def test_refresh_strips_html_from_excerpt_without_paraphrasing(db_session):
    python_blog, github_blog = _sources(db_session)
    respx.get(python_blog.url).mock(return_value=httpx.Response(200, content=PYTHON_BLOG_XML))
    respx.get(github_blog.url).mock(return_value=httpx.Response(200, content=GITHUB_BLOG_XML))

    _service(db_session).refresh()

    item = NewsItemRepository(db_session).get_by_link("https://github.blog/a-guide/")
    assert item.excerpt == "Go beyond chat with these slash commands ."


@respx.mock
def test_refresh_is_idempotent_by_link(db_session):
    python_blog, github_blog = _sources(db_session)
    respx.get(python_blog.url).mock(return_value=httpx.Response(200, content=PYTHON_BLOG_XML))
    respx.get(github_blog.url).mock(return_value=httpx.Response(200, content=GITHUB_BLOG_XML))
    service = _service(db_session)

    first = service.refresh()
    second = service.refresh()

    assert first.items_new_total == 3
    assert second.items_new_total == 0  # nothing new, same items already persisted
    assert len(NewsItemRepository(db_session).list_recent()) == 3


@respx.mock
def test_refresh_isolates_a_failing_source_from_the_others(db_session):
    python_blog, github_blog = _sources(db_session)
    respx.get(python_blog.url).mock(return_value=httpx.Response(500))
    respx.get(github_blog.url).mock(return_value=httpx.Response(200, content=GITHUB_BLOG_XML))

    summary = _service(db_session).refresh()

    by_key = {r.source_key: r for r in summary.results}
    assert by_key["python_blog"].error is not None
    assert by_key["github_blog"].error is None
    assert by_key["github_blog"].items_new == 1
    assert len(NewsItemRepository(db_session).list_recent()) == 1


def test_news_service_has_no_ai_dependency():
    """Structural guarantee, not just an omission: NewsService.__init__
    only accepts repositories — there is no AIService/LLMProvider
    parameter for a caller to even pass, so no code path here can ever
    reach the model. See docs/adr/0014-defer-ai-summarization.md.
    """
    import inspect

    params = inspect.signature(NewsService.__init__).parameters
    assert set(params) == {"self", "source_repo", "news_item_repo"}
