"""News endpoints — see docs/08-modules/news-intelligence.md and
docs/09-backend/api-design.md.

Thin router: all orchestration lives in NewsService, all persistence in
Source/NewsItemRepository (see docs/09-backend/architecture.md layer
rules). Authenticated like every other application endpoint since Gate 2
— not because the digest is per-user (it isn't, no personalization exists
yet), but for consistency with the rest of the API surface and to avoid
exposing a new public surface unnecessarily. No News-specific permission
scope exists — this reuses the same `get_current_user` dependency as
everything else, per the Gate 5 GO instruction not to invent one the
documentation doesn't call for.
"""
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_news_item_repository, get_news_service, get_source_repository
from app.models.user import User
from app.repositories.news_item_repository import NewsItemRepository
from app.repositories.source_repository import SourceRepository
from app.schemas.news import NewsItemResponse, RefreshResponse, SourceRefreshResultResponse
from app.services.news_service import NewsService

router = APIRouter()


@router.post("/refresh", response_model=RefreshResponse)
def refresh(
    current_user: User = Depends(get_current_user),
    service: NewsService = Depends(get_news_service),
) -> RefreshResponse:
    summary = service.refresh()
    return RefreshResponse(
        results=[
            SourceRefreshResultResponse(
                source_key=r.source_key, items_found=r.items_found, items_new=r.items_new, error=r.error
            )
            for r in summary.results
        ],
        items_new_total=summary.items_new_total,
    )


@router.get("", response_model=list[NewsItemResponse])
def list_digest(
    current_user: User = Depends(get_current_user),
    news_item_repo: NewsItemRepository = Depends(get_news_item_repository),
    source_repo: SourceRepository = Depends(get_source_repository),
) -> list[NewsItemResponse]:
    source_names = {s.id: s.name for s in source_repo.list_all()}
    items = news_item_repo.list_recent()
    return [
        NewsItemResponse(
            id=str(item.id),
            title=item.title,
            link=item.link,
            excerpt=item.excerpt,
            source_name=source_names.get(item.source_id, "Unknown source"),
            published_at=item.published_at,
        )
        for item in items
    ]
