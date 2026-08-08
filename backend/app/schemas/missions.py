"""Request/response shapes for POST /api/v1/missions.

`MissionRequest` deliberately has exactly one field. There is structurally
no `user_id`, `xp_awarded`, `permission`, `risk`, or `agent_name` field to
accept — Pydantic drops unrecognized keys by default, so even a client that
sends them has no way to influence anything (see
tests/test_missions_api.py for the regression test proving this).
"""
from pydantic import BaseModel, Field

from app.schemas.agents import ResearchSource


class MissionRequest(BaseModel):
    goal: str = Field(min_length=1, max_length=2000)


class MissionResponse(BaseModel):
    id: str
    status: str
    answer: str
    sources: list[ResearchSource] = []
    xp_awarded: int
    failure_reason: str | None = None
