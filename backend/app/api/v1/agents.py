"""Agent endpoints — see docs/09-backend/api-design.md (/api/v1/agents group).

Thin router: all orchestration lives in ResearchAgent, not here (see
docs/09-backend/architecture.md layer rules). Requires authentication —
unlike Phase 0's /ai/chat, this endpoint performs permissioned, audited
actions, so "who" must be real.
"""
from fastapi import APIRouter, Depends

from app.agents.research_agent import ResearchAgent
from app.api.deps import get_current_user, get_research_agent
from app.models.user import User
from app.schemas.agents import ResearchRequest, ResearchResponse

router = APIRouter()


@router.post("/research", response_model=ResearchResponse)
def research(
    payload: ResearchRequest,
    current_user: User = Depends(get_current_user),
    agent: ResearchAgent = Depends(get_research_agent),
) -> ResearchResponse:
    result = agent.research(payload.query, user_id=current_user.id, confirmed=payload.confirmed)
    return ResearchResponse(
        answer=result.answer,
        sources=result.sources,
        audit_id=str(result.audit_id) if result.audit_id else None,
        outcome=result.outcome,
    )
