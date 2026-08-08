"""Request/response shapes for /api/v1/news — see docs/08-modules/news-intelligence.md.

No request body exists for POST /news/refresh — there is nothing for a
client to supply an authority value through (source, URL, etc.), matching
the pattern already used by MissionRequest/SendMessageRequest.
"""
from datetime import datetime

from pydantic import BaseModel


class NewsItemResponse(BaseModel):
    id: str
    title: str
    link: str
    excerpt: str | None = None
    source_name: str
    published_at: datetime | None = None


class SourceRefreshResultResponse(BaseModel):
    source_key: str
    items_found: int
    items_new: int
    error: str | None = None


class RefreshResponse(BaseModel):
    results: list[SourceRefreshResultResponse]
    items_new_total: int
