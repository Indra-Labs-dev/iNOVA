"""ResearchAgent orchestration tests. LLM responses are faked (deterministic,
no network) — read_rss_feed's own HTTP call is mocked via respx where a real
tool execution is needed. This is exactly the "mock RSS, not a real site"
integration test required for Gate 2 (docs/14-testing/agent-tests.md).

Security tests (the Gate 2 "Ne masque aucun échec" requirement) live here
too: hallucinated tool, invalid arguments, and permission-denied must all
result in NO execution and a recorded audit entry.
"""
import uuid

import httpx
import respx

from app.agents.research_agent import AGENT_NAME, ResearchAgent
from app.ai.provider import LLMProvider
from app.ai.types import LLMResponse, ToolCall, ToolCallOutcome
from app.models.audit_log import AuditOutcome
from app.repositories.audit_log_repository import AuditLogRepository
from app.tools.registry import RegisteredTool, ToolRegistry
from app.tools.research_tools import RSS_ALLOWLIST, READ_RSS_FEED, read_rss_feed_handler

VALID_RSS = b"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>Python Insider</title>
<item><title>Python 3.14 released</title><link>https://blog.python.org/1</link><pubDate>Mon, 01 Jan 2026 00:00:00 GMT</pubDate></item>
</channel></rss>"""


class ScriptedLLM(LLMProvider):
    """Returns whatever LLMResponse the test configures — bypasses real
    Ollama text parsing entirely, since that's already covered by
    test_tool_call_parsing.py and test_llm_provider.py. This test suite is
    about ResearchAgent's orchestration, not the parser."""

    model = "scripted-llm"

    def __init__(self, responses: list[LLMResponse]):
        self._responses = list(responses)
        self.calls: list[dict] = []

    def generate(self, message, tools=None, system=None) -> LLMResponse:
        self.calls.append({"message": message, "tools": tools, "system": system})
        return self._responses.pop(0)


def _registry_with_rss_tool() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(RegisteredTool(definition=READ_RSS_FEED, handler=read_rss_feed_handler))
    return registry


@respx.mock
def test_successful_research_returns_synthesized_answer_and_sources(db_session):
    respx.get(RSS_ALLOWLIST["python_blog"]).mock(return_value=httpx.Response(200, content=VALID_RSS))
    llm = ScriptedLLM(
        [
            LLMResponse(
                content=None,
                tool_call=ToolCall(name="read_rss_feed", arguments={"feed_id": "python_blog"}),
                tool_call_outcome=ToolCallOutcome.VALID,
            ),
            LLMResponse(content="Python 3.14 was just released.", tool_call=None),
        ]
    )
    from app.ai.service import AIService

    agent = ResearchAgent(AIService(llm), _registry_with_rss_tool(), AuditLogRepository(db_session))
    user_id = uuid.uuid4()

    result = agent.research("What's new for Python?", user_id=user_id)

    assert result.outcome == AuditOutcome.SUCCESS.value
    assert result.answer == "Python 3.14 was just released."
    assert result.sources[0]["title"] == "Python 3.14 released"
    assert result.audit_id is not None

    audit_repo = AuditLogRepository(db_session)
    entries = audit_repo.list_for_user(user_id)
    assert len(entries) == 1
    assert entries[0].outcome == AuditOutcome.SUCCESS.value
    assert entries[0].tool_name == "read_rss_feed"
    assert entries[0].agent_name == AGENT_NAME


def test_plain_answer_with_no_tool_needed_is_not_audited(db_session):
    from app.ai.service import AIService

    llm = ScriptedLLM([LLMResponse(content="I can only help with research topics.", tool_call=None)])
    agent = ResearchAgent(AIService(llm), _registry_with_rss_tool(), AuditLogRepository(db_session))
    user_id = uuid.uuid4()

    result = agent.research("Hello!", user_id=user_id)

    assert result.answer == "I can only help with research topics."
    assert result.audit_id is None
    assert AuditLogRepository(db_session).list_for_user(user_id) == []


def test_hallucinated_tool_is_blocked_and_audited(db_session):
    from app.ai.service import AIService

    # Simulates exactly what OllamaProvider returns for a hallucinated tool
    # name per docs/adr/0012 — content preserved, tool_call is None.
    llm = ScriptedLLM(
        [LLMResponse(content='{"name": "search_online", "arguments": {}}', tool_call=None, tool_call_outcome=ToolCallOutcome.UNKNOWN_TOOL)]
    )
    agent = ResearchAgent(AIService(llm), _registry_with_rss_tool(), AuditLogRepository(db_session))
    user_id = uuid.uuid4()

    result = agent.research("What is 12 times 7?", user_id=user_id)

    assert result.outcome == AuditOutcome.INVALID_TOOL_CALL.value
    entries = AuditLogRepository(db_session).list_for_user(user_id)
    assert len(entries) == 1
    assert entries[0].success is False
    assert entries[0].outcome == AuditOutcome.INVALID_TOOL_CALL.value


def test_invalid_arguments_is_blocked_and_audited(db_session):
    from app.ai.service import AIService

    llm = ScriptedLLM(
        [LLMResponse(content='{"name": "read_rss_feed", "arguments": {}}', tool_call=None, tool_call_outcome=ToolCallOutcome.INVALID_ARGUMENTS)]
    )
    agent = ResearchAgent(AIService(llm), _registry_with_rss_tool(), AuditLogRepository(db_session))
    user_id = uuid.uuid4()

    result = agent.research("Read the feed", user_id=user_id)

    assert result.outcome == AuditOutcome.INVALID_ARGUMENTS.value
    assert AuditLogRepository(db_session).list_for_user(user_id)[0].success is False


def test_permission_denied_blocks_execution_end_to_end(db_session):
    from app.ai.service import AIService

    llm = ScriptedLLM(
        [
            LLMResponse(
                content=None,
                tool_call=ToolCall(name="read_rss_feed", arguments={"feed_id": "python_blog"}),
                tool_call_outcome=ToolCallOutcome.VALID,
            )
        ]
    )
    agent = ResearchAgent(
        AIService(llm),
        _registry_with_rss_tool(),
        AuditLogRepository(db_session),
        granted_permissions=set(),  # simulate a caller without research.read
    )
    user_id = uuid.uuid4()

    with respx.mock:
        # If execution were mistakenly allowed, this route would be hit —
        # asserting no route registered means any real request raises.
        result = agent.research("Read the feed", user_id=user_id)

    assert result.outcome == AuditOutcome.PERMISSION_DENIED.value
    entries = AuditLogRepository(db_session).list_for_user(user_id)
    assert entries[0].outcome == AuditOutcome.PERMISSION_DENIED.value


def test_tool_execution_failure_is_audited_but_not_treated_as_success(db_session):
    from app.ai.service import AIService

    respx_mock = respx.mock
    with respx_mock:
        respx.get(RSS_ALLOWLIST["python_blog"]).mock(return_value=httpx.Response(503))
        llm = ScriptedLLM(
            [
                LLMResponse(
                    content=None,
                    tool_call=ToolCall(name="read_rss_feed", arguments={"feed_id": "python_blog"}),
                    tool_call_outcome=ToolCallOutcome.VALID,
                )
            ]
        )
        agent = ResearchAgent(AIService(llm), _registry_with_rss_tool(), AuditLogRepository(db_session))
        user_id = uuid.uuid4()

        result = agent.research("Read the feed", user_id=user_id)

    assert result.outcome == AuditOutcome.EXECUTION_FAILED.value
    entries = AuditLogRepository(db_session).list_for_user(user_id)
    assert entries[0].success is False
    assert entries[0].outcome == AuditOutcome.EXECUTION_FAILED.value


def test_model_supplied_permission_or_risk_fields_are_ignored():
    # Structural security property: ToolCall only ever carries name+arguments
    # — even if the model's JSON includes extra keys trying to claim a
    # permission or risk level, they are never parsed into the ToolCall at
    # all (see app/ai/tool_call_parsing.py) — there is no field for them to
    # land in. This test documents that guarantee at the type level.
    call = ToolCall(name="read_rss_feed", arguments={"feed_id": "python_blog"})
    assert not hasattr(call, "permission")
    assert not hasattr(call, "risk")
    assert not hasattr(call, "confirmation_required")
