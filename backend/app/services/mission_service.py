"""MissionService — orchestration layer on top of ResearchAgent, per
docs/08-modules/mission-system.md MVP scope: one goal, one step, one agent.

This is NOT a second AI/agent/permission implementation — it calls
`ResearchAgent.research()` as a black box and only interprets its already-
validated, already-audited result. No tool call, no LLM prompt, no
permission check happens here; duplicating any of that would violate
docs/07-agents/agent-security.md's single-source-of-truth principle.
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.agents.research_agent import AGENT_NAME, ResearchAgent
from app.models.audit_log import AuditOutcome
from app.models.mission import Mission, MissionStatus
from app.repositories.mission_repository import MissionRepository
from app.repositories.user_progress_repository import UserProgressRepository

MISSION_SUCCESS_XP = 10


@dataclass(frozen=True)
class MissionOutcome:
    """Mission + the sources used to complete it. Sources are NOT persisted
    on the Mission row (keeping the schema minimal, per docs/08-modules/
    mission-system.md — no over-normalization for a deferred GET endpoint);
    this is the one place a caller can still see them, right after creation.
    """

    mission: Mission
    sources: list[dict] = field(default_factory=list)


class MissionService:
    def __init__(
        self,
        research_agent: ResearchAgent,
        mission_repo: MissionRepository,
        user_progress_repo: UserProgressRepository,
    ):
        self._research_agent = research_agent
        self._mission_repo = mission_repo
        self._user_progress_repo = user_progress_repo

    def start(self, goal: str, user_id: uuid.UUID) -> MissionOutcome:
        """Synchronous end to end (no queue/scheduler at this Gate — see
        docs/08-modules/mission-system.md): by the time this returns, the
        mission is already in its final state. `user_id` always comes from
        the authenticated request context (see app/api/v1/missions.py),
        never from the request body.
        """
        result = self._research_agent.research(goal, user_id=user_id)

        if result.outcome == AuditOutcome.SUCCESS.value:
            status = MissionStatus.COMPLETED.value
            failure_reason = None
            xp_awarded = MISSION_SUCCESS_XP
            self._user_progress_repo.add_xp(user_id, xp_awarded)
        else:
            # ResearchAgent's own outcome is preserved verbatim, never
            # collapsed into a generic failure — see docs/08-modules/
            # mission-system.md "Mission status".
            status = MissionStatus.FAILED.value
            failure_reason = result.outcome
            xp_awarded = 0

        mission = self._mission_repo.create(
            user_id=user_id,
            goal=goal,
            agent_name=AGENT_NAME,
            status=status,
            answer=result.answer,
            xp_awarded=xp_awarded,
            failure_reason=failure_reason,
            audit_id=result.audit_id,
            completed_at=datetime.now(timezone.utc),
        )
        return MissionOutcome(mission=mission, sources=result.sources)
