"""read_rss_feed handler tests — all network mocked via respx, per
docs/14-testing/agent-tests.md. Covers docs 07-agents/agents/research-agent.md
"Errors" and the SSRF-prevention requirement (feed_id only, never a URL).
"""
import httpx
import respx

from app.tools.research_tools import RSS_ALLOWLIST, read_rss_feed_handler

VALID_RSS = b"""<?xml version="1.0"?>
<rss version="2.0"><channel>
<title>Test Feed</title>
<item><title>First Post</title><link>https://example.com/1</link><pubDate>Mon, 01 Jan 2026 00:00:00 GMT</pubDate></item>
<item><title>Second Post</title><link>https://example.com/2</link><pubDate>Tue, 02 Jan 2026 00:00:00 GMT</pubDate></item>
</channel></rss>"""


def test_unknown_feed_id_is_rejected_without_any_network_call():
    result = read_rss_feed_handler({"feed_id": "not_a_real_feed"})

    assert result.success is False
    assert "not an allowlisted feed" in result.error


def test_url_smuggled_as_feed_id_is_rejected_without_any_network_call():
    # The whole point of the feed_id design: even if something bypasses the
    # JSON-schema enum check upstream, the handler itself never treats an
    # arbitrary string as a URL.
    result = read_rss_feed_handler({"feed_id": "http://169.254.169.254/latest/meta-data"})

    assert result.success is False
    assert "not an allowlisted feed" in result.error


@respx.mock
def test_allowlisted_feed_returns_parsed_items():
    url = RSS_ALLOWLIST["python_blog"]
    respx.get(url).mock(return_value=httpx.Response(200, content=VALID_RSS))

    result = read_rss_feed_handler({"feed_id": "python_blog"})

    assert result.success is True
    assert result.data["items"][0]["title"] == "First Post"
    assert len(result.data["items"]) == 2
    assert "First Post" in result.summary


@respx.mock
def test_invalid_rss_xml_is_reported_as_failure_not_crash():
    url = RSS_ALLOWLIST["python_blog"]
    respx.get(url).mock(return_value=httpx.Response(200, content=b"not xml at all {{{"))

    result = read_rss_feed_handler({"feed_id": "python_blog"})

    assert result.success is False
    assert "invalid RSS" in result.error


@respx.mock
def test_http_error_status_is_reported_as_failure():
    url = RSS_ALLOWLIST["github_blog"]
    respx.get(url).mock(return_value=httpx.Response(503))

    result = read_rss_feed_handler({"feed_id": "github_blog"})

    assert result.success is False
    assert "503" in result.error


@respx.mock
def test_timeout_is_reported_as_failure():
    url = RSS_ALLOWLIST["github_blog"]
    respx.get(url).mock(side_effect=httpx.TimeoutException("timed out"))

    result = read_rss_feed_handler({"feed_id": "github_blog"})

    assert result.success is False
    assert "Timed out" in result.error


@respx.mock
def test_empty_feed_is_a_success_with_no_items():
    url = RSS_ALLOWLIST["python_blog"]
    empty_rss = b'<?xml version="1.0"?><rss version="2.0"><channel><title>Empty</title></channel></rss>'
    respx.get(url).mock(return_value=httpx.Response(200, content=empty_rss))

    result = read_rss_feed_handler({"feed_id": "python_blog"})

    assert result.success is True
    assert result.data["items"] == []


@respx.mock
def test_does_not_follow_redirects():
    url = RSS_ALLOWLIST["python_blog"]
    route = respx.get(url).mock(return_value=httpx.Response(200, content=VALID_RSS))

    read_rss_feed_handler({"feed_id": "python_blog"})

    assert route.calls[0].request.url == httpx.URL(url)
