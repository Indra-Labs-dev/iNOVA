"""read_rss_feed — the only real tool in Phase 1 (docs/07-agents/agents/research-agent.md).

SSRF prevention (docs/12-security/network-security.md): the model NEVER
supplies a URL. Its only input is `feed_id`, constrained by JSON Schema
`enum` to the allowlist keys below, re-validated defensively inside the
handler (never trust that upstream validation caught everything — the LLM's
output is untrusted at every layer, not just the first one that sees it).
The backend resolves `feed_id` to a URL from server-side configuration; an
attacker (or a hallucinating model) cannot smuggle `http://169.254.169.254/...`
or any other destination through this path, because no argument ever
becomes part of the outbound request URL.

No general crawler, no arbitrary fetch, no web search — explicitly out of
scope for Phase 1 (see docs/07-agents/agents/research-agent.md "Tools").
"""
import xml.etree.ElementTree as ET

import httpx

from app.ai.types import ToolDefinition
from app.tools.registry import RegisteredTool, ToolExecutionResult, default_registry

# Server-side only — never derived from user or model input. Two official,
# stable, first-party sources (docs/11-intelligence/scraping-policy.md:
# prefer official sources). Add entries only via a code change + review.
RSS_ALLOWLIST: dict[str, str] = {
    "python_blog": "https://blog.python.org/feeds/posts/default",
    "github_blog": "https://github.blog/feed/",
}

_MAX_ITEMS = 5
_REQUEST_TIMEOUT_SECONDS = 10.0
_MAX_RESPONSE_BYTES = 2_000_000  # 2MB ceiling — a feed this large is not legitimate use


def _parse_rss_items(xml_bytes: bytes) -> list[dict[str, str]]:
    root = ET.fromstring(xml_bytes)  # noqa: S314 — trusted, allowlisted sources only
    items = []
    for item in root.findall("./channel/item")[:_MAX_ITEMS]:
        title = item.findtext("title", default="").strip()
        link = item.findtext("link", default="").strip()
        pub_date = item.findtext("pubDate", default="").strip()
        items.append({"title": title, "link": link, "published": pub_date})
    return items


def read_rss_feed_handler(arguments: dict) -> ToolExecutionResult:
    feed_id = arguments.get("feed_id")

    # Defensive re-check — never trust that JSON-schema validation upstream
    # was the only gate (docs/adr/0012-tool-calling-contract.md).
    url = RSS_ALLOWLIST.get(feed_id)
    if url is None:
        return ToolExecutionResult(
            success=False, summary="", error=f"'{feed_id}' is not an allowlisted feed."
        )

    try:
        response = httpx.get(
            url,
            timeout=_REQUEST_TIMEOUT_SECONDS,
            follow_redirects=False,  # never follow off-allowlist redirects
        )
        response.raise_for_status()
    except httpx.TimeoutException:
        return ToolExecutionResult(success=False, summary="", error=f"Timed out fetching '{feed_id}'.")
    except httpx.HTTPStatusError as exc:
        return ToolExecutionResult(
            success=False, summary="", error=f"'{feed_id}' returned HTTP {exc.response.status_code}."
        )
    except httpx.HTTPError as exc:
        return ToolExecutionResult(success=False, summary="", error=f"Failed to fetch '{feed_id}': {exc}")

    if len(response.content) > _MAX_RESPONSE_BYTES:
        return ToolExecutionResult(success=False, summary="", error=f"'{feed_id}' response exceeded size limit.")

    try:
        items = _parse_rss_items(response.content)
    except ET.ParseError as exc:
        return ToolExecutionResult(success=False, summary="", error=f"'{feed_id}' returned invalid RSS: {exc}")

    if not items:
        return ToolExecutionResult(success=True, summary=f"No items found in '{feed_id}'.", data={"items": []})

    summary = f"{len(items)} item(s) from '{feed_id}': " + "; ".join(i["title"] for i in items if i["title"])
    return ToolExecutionResult(success=True, summary=summary[:500], data={"feed_id": feed_id, "items": items})


READ_RSS_FEED = ToolDefinition(
    name="read_rss_feed",
    description=(
        "Fetch recent items from one of iNOVA's allowlisted RSS feeds. "
        "You must choose feed_id from the allowed list — you cannot supply a URL."
    ),
    input_schema={
        "type": "object",
        "properties": {
            "feed_id": {
                "type": "string",
                "description": "Identifier of an allowlisted feed.",
                "enum": list(RSS_ALLOWLIST.keys()),
            }
        },
        "required": ["feed_id"],
    },
    permission="research.read",
    risk="LOW",
    confirmation_required=False,
)

default_registry.register(RegisteredTool(definition=READ_RSS_FEED, handler=read_rss_feed_handler))
