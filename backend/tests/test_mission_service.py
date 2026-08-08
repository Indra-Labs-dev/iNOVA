"""MissionService orchestration tests — ResearchAgent is faked (no LLM, no
network), mirroring the pattern in test_research_agent.py. This suite is
about Mission's own logic (status/failure_reason/XP mapping), not
ResearchAgent's, which is already covered elsewhere.
"""
import uuid

import pytest

from app.agents.research_agent import ResearchResult
from app.models.audit_log import AuditOutcome
from app.models.mission import MissionStatus
from app.repositories.mission_repository import MissionRepository
from app.repositories.user_progress_repository import UserProgressRepository
from app.services.mission_service import MISSION_SUCCESS_XP, MissionService


class FakeResearchAgent:
    def __init__(self, result: ResearchResult):
        self._result = result
        self.calls: list[dict] = []

    def research(self, query, user_id, confirmed=False):
        self.calls.append({"query": query, "user_id": user_id, "confirmed": confirmed})
        return self._result


def _service(db_session, result: ResearchResult) -> tuple[MissionService, FakeResearchAgent]:
    agent = FakeResearchAgent(result)
    service = MissionService(agent, MissionRepository(db_session), UserProgressRepository(db_session))
    return service, agent


def test_successful_mission_is_completed_and_awards_xp(db_session):
    result = ResearchResult(
        answer="Python 3.14 was released.",
        sources=[{"title": "Python 3.14 released", "link": "https://blog.python.org/1"}],
        audit_id=uuid.uuid4(),
        outcome=AuditOutcome.SUCCESS.value,
    )
    service, agent = _service(db_session, result)
    user_id = uuid.uuid4()

    mission = service.start("What's new for Python?", user_id=user_id)

    assert mission.status == MissionStatus.COMPLETED.value
    assert mission.xp_awarded == MISSION_SUCCESS_XP
    assert mission.failure_reason is None
    assert mission.answer == "Python 3.14 was released."
    assert agent.calls[0]["user_id"] == user_id

    progress = UserProgressRepository(db_session).get(user_id)
    assert progress.xp == MISSION_SUCCESS_XP


@pytest.mark.parametrize(
    "outcome",
    [
        AuditOutcome.PERMISSION_DENIED.value,
        AuditOutcome.INVALID_TOOL_CALL.value,
        AuditOutcome.INVALID_ARGUMENTS.value,
        AuditOutcome.EXECUTION_FAILED.value,
    ],
)
def test_non_success_outcomes_are_failed_and_award_no_xp(db_session, outcome):
    result = ResearchResult(answer="Something went wrong.", sources=[], audit_id=None, outcome=outcome)
    service, _ = _service(db_session, result)
    user_id = uuid.uuid4()

    mission = service.start("Do something", user_id=user_id)

    assert mission.status == MissionStatus.FAILED.value
    assert mission.xp_awarded == 0
    # The underlying ResearchAgent outcome is preserved verbatim, not
    # collapsed into a generic "failed" message.
    assert mission.failure_reason == outcome

    assert UserProgressRepository(db_session).get(user_id) is None


def test_failed_mission_does_not_touch_user_progress_at_all(db_session):
    result = ResearchResult(answer="Denied.", sources=[], audit_id=None, outcome=AuditOutcome.PERMISSION_DENIED.value)
    service, _ = _service(db_session, result)
    user_id = uuid.uuid4()

    # Pre-existing XP must remain untouched by a failed mission.
    UserProgressRepository(db_session).add_xp(user_id, 50)

    service.start("Do something", user_id=user_id)

    assert UserProgressRepository(db_session).get(user_id).xp == 50


def test_repeated_successful_missions_accumulate_xp(db_session):
    result = ResearchResult(answer="ok", sources=[], audit_id=None, outcome=AuditOutcome.SUCCESS.value)
    service, _ = _service(db_session, result)
    user_id = uuid.uuid4()

    service.start("goal 1", user_id=user_id)
    service.start("goal 2", user_id=user_id)

    assert UserProgressRepository(db_session).get(user_id).xp == MISSION_SUCCESS_XP * 2
