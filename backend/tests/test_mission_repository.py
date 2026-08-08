import uuid
from datetime import datetime, timezone

from app.models.mission import MissionStatus
from app.repositories.mission_repository import MissionRepository


def test_create_completed_mission(db_session):
    repo = MissionRepository(db_session)
    user_id = uuid.uuid4()

    mission = repo.create(
        user_id=user_id,
        goal="Give me the latest from python_blog.",
        agent_name="research_agent",
        status=MissionStatus.COMPLETED.value,
        answer="Python 3.14 was released.",
        xp_awarded=10,
        failure_reason=None,
        audit_id=uuid.uuid4(),
        completed_at=datetime.now(timezone.utc),
    )

    assert mission.id is not None
    assert mission.status == MissionStatus.COMPLETED.value
    assert mission.xp_awarded == 10
    assert mission.failure_reason is None


def test_create_failed_mission_preserves_failure_reason(db_session):
    repo = MissionRepository(db_session)

    mission = repo.create(
        user_id=uuid.uuid4(),
        goal="Do something not permitted.",
        agent_name="research_agent",
        status=MissionStatus.FAILED.value,
        answer="You don't have permission to use this capability.",
        xp_awarded=0,
        failure_reason="permission_denied",
        audit_id=None,
        completed_at=datetime.now(timezone.utc),
    )

    assert mission.status == MissionStatus.FAILED.value
    assert mission.xp_awarded == 0
    assert mission.failure_reason == "permission_denied"


def test_get_by_id_returns_none_for_unknown_id(db_session):
    assert MissionRepository(db_session).get_by_id(uuid.uuid4()) is None


def test_list_for_user_scoped_and_ordered_most_recent_first(db_session):
    repo = MissionRepository(db_session)
    user_a = uuid.uuid4()
    user_b = uuid.uuid4()

    def _create(user_id, goal):
        return repo.create(
            user_id=user_id,
            goal=goal,
            agent_name="research_agent",
            status=MissionStatus.COMPLETED.value,
            answer="ok",
            xp_awarded=10,
            failure_reason=None,
            audit_id=None,
            completed_at=datetime.now(timezone.utc),
        )

    _create(user_a, "first")
    _create(user_b, "other user")
    _create(user_a, "second")

    missions = repo.list_for_user(user_a)

    assert len(missions) == 2
    assert missions[0].goal == "second"
    assert missions[1].goal == "first"
