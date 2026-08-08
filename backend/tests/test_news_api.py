"""API-layer tests for /api/v1/news — mirrors tests/test_missions_api.py's
pattern (real register/login flow), respx-mocked RSS (no real network).
"""
import uuid

import httpx
import respx

from app.models.source import Source

PYTHON_BLOG_XML = b"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>Python Insider</title>
<item>
<title>Python 3.14.7 and 3.13.15 are now available!</title>
<link>https://blog.python.org/2026/08/python-3147-31315/</link>
<description>A pair of bug fix releases await your upgrade.</description>
<pubDate>Wed, 05 Aug 2026 00:00:00 GMT</pubDate>
</item>
</channel></rss>"""


def _register_and_login(client, email="reader@inova.dev"):
    client.post("/api/v1/auth/register", json={"email": email, "password": "correct-horse-battery"})
    tokens = client.post("/api/v1/auth/login", json={"email": email, "password": "correct-horse-battery"}).json()
    return tokens["access_token"]


def _auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def _seed_source(db_session) -> Source:
    source = Source(
        id=uuid.uuid4(), key="python_blog", name="Python Insider", url="https://blog.python.org/feed"
    )
    db_session.add(source)
    db_session.commit()
    return source


def test_refresh_requires_authentication(client):
    response = client.post("/api/v1/news/refresh")
    assert response.status_code == 401


def test_digest_requires_authentication(client):
    response = client.get("/api/v1/news")
    assert response.status_code == 401


@respx.mock
def test_refresh_persists_items_and_digest_reflects_them(client, db_session):
    source = _seed_source(db_session)
    respx.get(source.url).mock(return_value=httpx.Response(200, content=PYTHON_BLOG_XML))
    token = _register_and_login(client)

    refresh_response = client.post("/api/v1/news/refresh", headers=_auth_headers(token))
    assert refresh_response.status_code == 200
    body = refresh_response.json()
    assert body["items_new_total"] == 1
    assert body["results"][0]["source_key"] == "python_blog"
    assert body["results"][0]["error"] is None

    digest_response = client.get("/api/v1/news", headers=_auth_headers(token))
    assert digest_response.status_code == 200
    items = digest_response.json()
    assert len(items) == 1
    assert items[0]["title"] == "Python 3.14.7 and 3.13.15 are now available!"
    assert items[0]["excerpt"] == "A pair of bug fix releases await your upgrade."
    assert items[0]["source_name"] == "Python Insider"
    assert items[0]["link"] == "https://blog.python.org/2026/08/python-3147-31315/"


@respx.mock
def test_refresh_is_idempotent_across_two_calls(client, db_session):
    source = _seed_source(db_session)
    respx.get(source.url).mock(return_value=httpx.Response(200, content=PYTHON_BLOG_XML))
    token = _register_and_login(client, email="idempotent@inova.dev")

    first = client.post("/api/v1/news/refresh", headers=_auth_headers(token)).json()
    second = client.post("/api/v1/news/refresh", headers=_auth_headers(token)).json()

    assert first["items_new_total"] == 1
    assert second["items_new_total"] == 0

    digest = client.get("/api/v1/news", headers=_auth_headers(token)).json()
    assert len(digest) == 1


def test_refresh_ignores_any_client_supplied_body(client, db_session):
    """POST /news/refresh declares no request body — there is no field for
    a client to supply a source/URL/authority value through, and an
    attempted body has zero effect (structurally, not by validation).
    """
    _seed_source(db_session)
    token = _register_and_login(client, email="spoofer@inova.dev")

    with respx.mock:
        respx.get("https://blog.python.org/feed").mock(return_value=httpx.Response(200, content=PYTHON_BLOG_XML))
        response = client.post(
            "/api/v1/news/refresh",
            json={"url": "http://169.254.169.254/latest/meta-data/", "source": "evil"},
            headers=_auth_headers(token),
        )

    assert response.status_code == 200
    # Only the real seeded source was ever touched — nothing from the body.
    assert response.json()["results"][0]["source_key"] == "python_blog"


@respx.mock
def test_digest_never_exposes_full_article_content(client, db_session):
    """Regression for the scraping-policy.md rule: summarize/attribute,
    never republish full source text. Since AI summarization is deferred,
    the excerpt is the RSS description as-is (already short) — this test
    guards against a future change accidentally piping full body content
    into the digest.
    """
    source = _seed_source(db_session)
    respx.get(source.url).mock(return_value=httpx.Response(200, content=PYTHON_BLOG_XML))
    token = _register_and_login(client, email="attribution@inova.dev")

    client.post("/api/v1/news/refresh", headers=_auth_headers(token))
    items = client.get("/api/v1/news", headers=_auth_headers(token)).json()

    assert len(items[0]["excerpt"]) < 500
