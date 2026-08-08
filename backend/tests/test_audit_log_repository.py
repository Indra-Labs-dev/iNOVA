import uuid

from app.models.audit_log import AuditOutcome
from app.repositories.audit_log_repository import AuditLogRepository


def test_record_success_entry(db_session):
    repo = AuditLogRepository(db_session)
    user_id = uuid.uuid4()

    entry = repo.record(
        user_id=user_id,
        agent_name="research_agent",
        outcome=AuditOutcome.SUCCESS,
        success=True,
        tool_name="read_rss_feed",
        permission="research.read",
        risk="LOW",
        result_summary="Fetched 5 items from python_blog.",
    )

    assert entry.id is not None
    assert entry.success is True
    assert entry.outcome == AuditOutcome.SUCCESS.value
    assert entry.user_id == user_id


def test_record_permission_denied_entry_has_no_tool_execution_detail(db_session):
    repo = AuditLogRepository(db_session)

    entry = repo.record(
        user_id=uuid.uuid4(),
        agent_name="research_agent",
        outcome=AuditOutcome.PERMISSION_DENIED,
        success=False,
        tool_name="read_rss_feed",
        permission="research.read",
        result_summary="User lacks research.read scope.",
    )

    assert entry.success is False
    assert entry.outcome == AuditOutcome.PERMISSION_DENIED.value


def test_record_truncates_overly_long_result_summary(db_session):
    repo = AuditLogRepository(db_session)

    entry = repo.record(
        user_id=uuid.uuid4(),
        agent_name="research_agent",
        outcome=AuditOutcome.SUCCESS,
        success=True,
        result_summary="x" * 1000,
    )

    assert len(entry.result_summary) == 500
    assert entry.result_summary.endswith("…")


def test_record_allows_null_user_and_tool_for_system_level_failures(db_session):
    repo = AuditLogRepository(db_session)

    entry = repo.record(
        user_id=None,
        agent_name="research_agent",
        outcome=AuditOutcome.INVALID_TOOL_CALL,
        success=False,
        result_summary="Model proposed an unregistered tool.",
    )

    assert entry.user_id is None
    assert entry.tool_name is None


def test_list_for_user_returns_only_that_users_entries_most_recent_first(db_session):
    repo = AuditLogRepository(db_session)
    user_a = uuid.uuid4()
    user_b = uuid.uuid4()

    repo.record(user_id=user_a, agent_name="research_agent", outcome=AuditOutcome.SUCCESS, success=True, result_summary="first")
    repo.record(user_id=user_b, agent_name="research_agent", outcome=AuditOutcome.SUCCESS, success=True, result_summary="other user")
    repo.record(user_id=user_a, agent_name="research_agent", outcome=AuditOutcome.SUCCESS, success=True, result_summary="second")

    entries = repo.list_for_user(user_a)

    assert len(entries) == 2
    assert entries[0].result_summary == "second"
    assert entries[1].result_summary == "first"


def test_get_by_id_returns_none_for_unknown_id(db_session):
    repo = AuditLogRepository(db_session)
    assert repo.get_by_id(uuid.uuid4()) is None
