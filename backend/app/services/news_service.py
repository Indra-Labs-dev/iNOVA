"""NewsService — Sources -> Collection -> Normalization -> Persistence ->
Feed (see docs/08-modules/news-intelligence.md). AI summarization is
explicitly NOT part of this pipeline — see docs/adr/0014-defer-ai-
summarization.md: measured (0/9 on the required fact/inference
distinction, plus one confirmed factual inversion) and deferred, not a
design preference. This service has no dependency on AIService or
LLMProvider at all — structurally, not just by omission, nothing here can
ever call the model.

Fetch logic intentionally does not share code with
app/tools/research_tools.py's read_rss_feed — that tool serves a different
consumer (an LLM-invoked ad-hoc lookup) with a different result shape and
its own test/security history; duplicating the same SSRF-safe pattern here
keeps the two independent rather than coupling Gate 2's tool to Gate 5's
pipeline.

Security: `Source.url` is only ever server-seeded (see the migration) —
nothing here, and nothing upstream of it, ever accepts a URL from a
client or from the model. See docs/11-intelligence/scraping-policy.md.
"""
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from email.utils import parsedate_to_datetime

import httpx

from app.models.source import Source
from app.repositories.news_item_repository import NewsItemRepository
from app.repositories.source_repository import SourceRepository

_MAX_ITEMS_PER_SOURCE = 10
_MAX_EXCERPT_CHARS = 1000
_REQUEST_TIMEOUT_SECONDS = 10.0
_MAX_RESPONSE_BYTES = 2_000_000  # 2MB ceiling — a feed this large is not legitimate use

_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")


def _strip_html(raw: str) -> str:
    """Normalization only — plain-text presentation of the source's own
    description, never a paraphrase or summary of it.
    """
    text = _TAG_RE.sub(" ", raw)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text[:_MAX_EXCERPT_CHARS]


def _parse_pub_date(raw: str) -> datetime | None:
    if not raw:
        return None
    try:
        return parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        return None


def _parse_feed_items(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)  # noqa: S314 — trusted, allowlisted sources only
    parsed = []
    for item in root.findall("./channel/item")[:_MAX_ITEMS_PER_SOURCE]:
        title = (item.findtext("title", default="") or "").strip()
        link = (item.findtext("link", default="") or "").strip()
        description = item.findtext("description", default="") or ""
        pub_date = _parse_pub_date((item.findtext("pubDate", default="") or "").strip())
        if not title or not link:
            continue
        parsed.append(
            {
                "title": title[:500],
                "link": link,
                "excerpt": _strip_html(description) or None,
                "published_at": pub_date,
            }
        )
    return parsed


@dataclass(frozen=True)
class SourceRefreshResult:
    source_key: str
    items_found: int = 0
    items_new: int = 0
    error: str | None = None


@dataclass(frozen=True)
class RefreshSummary:
    results: list[SourceRefreshResult] = field(default_factory=list)

    @property
    def items_new_total(self) -> int:
        return sum(r.items_new for r in self.results)


class NewsService:
    def __init__(self, source_repo: SourceRepository, news_item_repo: NewsItemRepository):
        self._source_repo = source_repo
        self._news_item_repo = news_item_repo

    def refresh(self) -> RefreshSummary:
        results = [self._refresh_one(source) for source in self._source_repo.list_all()]
        return RefreshSummary(results=results)

    def _refresh_one(self, source: Source) -> SourceRefreshResult:
        try:
            items = self._fetch_and_parse(source.url)
        except _FetchError as exc:
            return SourceRefreshResult(source_key=source.key, error=str(exc))

        items_new = 0
        for parsed in items:
            if self._news_item_repo.get_by_link(parsed["link"]) is not None:
                continue  # idempotent by URL — not the deferred semantic Deduplication stage
            self._news_item_repo.create(
                source_id=source.id,
                title=parsed["title"],
                link=parsed["link"],
                excerpt=parsed["excerpt"],
                published_at=parsed["published_at"],
            )
            items_new += 1

        return SourceRefreshResult(source_key=source.key, items_found=len(items), items_new=items_new)

    def _fetch_and_parse(self, url: str) -> list[dict]:
        try:
            response = httpx.get(
                url,
                timeout=_REQUEST_TIMEOUT_SECONDS,
                follow_redirects=False,  # never follow off-allowlist redirects
            )
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise _FetchError("Timed out fetching feed.") from exc
        except httpx.HTTPStatusError as exc:
            raise _FetchError(f"Feed returned HTTP {exc.response.status_code}.") from exc
        except httpx.HTTPError as exc:
            raise _FetchError(f"Failed to fetch feed: {exc}") from exc

        if len(response.content) > _MAX_RESPONSE_BYTES:
            raise _FetchError("Feed response exceeded size limit.")

        try:
            return _parse_feed_items(response.content)
        except ET.ParseError as exc:
            raise _FetchError(f"Feed returned invalid RSS: {exc}") from exc


class _FetchError(Exception):
    """Internal — a single source's failure never aborts the others."""
