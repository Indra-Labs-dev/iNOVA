"""Tests for the permission/confirmation authorization pipeline — this is
where Gate 1's rule ("LLM proposes, backend decides") becomes executable.

Uses a synthetic MEDIUM/HIGH test-only tool to prove the confirmation gate
works generically, WITHOUT giving ResearchAgent any real dangerous
capability — see the Gate 2 instructions: "Ne donne pas à ResearchAgent une
capacité dangereuse réelle simplement pour tester ce mécanisme." This tool
is never registered into app.tools.registry.default_registry.
"""
from app.ai.types import ToolCall, ToolDefinition
from app.tools.pipeline import PipelineOutcome, authorize_tool_call
from app.tools.registry import RegisteredTool, ToolExecutionResult, ToolRegistry

LOW_RISK_TOOL = ToolDefinition(
    name="read_rss_feed",
    description="",
    input_schema={"type": "object", "properties": {"feed_id": {"type": "string"}}, "required": ["feed_id"]},
    permission="research.read",
    risk="LOW",
    confirmation_required=False,
)

# Synthetic only — performs no action, exists solely to prove the
# confirmation gate mechanism handles MEDIUM/HIGH risk generically.
SYNTHETIC_HIGH_RISK_TOOL = ToolDefinition(
    name="synthetic_test_tool",
    description="Test-only tool; does nothing. Never registered in production.",
    input_schema={"type": "object", "properties": {}},
    permission="test.synthetic",
    risk="HIGH",
    confirmation_required=True,
)


def _noop_handler(args: dict) -> ToolExecutionResult:
    return ToolExecutionResult(success=True, summary="noop")


def _registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(RegisteredTool(definition=LOW_RISK_TOOL, handler=_noop_handler))
    registry.register(RegisteredTool(definition=SYNTHETIC_HIGH_RISK_TOOL, handler=_noop_handler))
    return registry


def test_low_risk_tool_allowed_with_correct_permission_no_confirmation_needed():
    decision = authorize_tool_call(
        ToolCall(name="read_rss_feed", arguments={"feed_id": "python_blog"}),
        registry=_registry(),
        granted_permissions={"research.read"},
    )

    assert decision.outcome == PipelineOutcome.ALLOWED
    assert decision.is_allowed


def test_missing_permission_denies_regardless_of_risk():
    decision = authorize_tool_call(
        ToolCall(name="read_rss_feed", arguments={"feed_id": "python_blog"}),
        registry=_registry(),
        granted_permissions=set(),  # no permissions granted at all
    )

    assert decision.outcome == PipelineOutcome.PERMISSION_DENIED
    assert not decision.is_allowed


def test_high_risk_tool_without_confirmation_is_blocked():
    decision = authorize_tool_call(
        ToolCall(name="synthetic_test_tool", arguments={}),
        registry=_registry(),
        granted_permissions={"test.synthetic"},
        confirmed=False,
    )

    assert decision.outcome == PipelineOutcome.CONFIRMATION_REQUIRED
    assert not decision.is_allowed


def test_high_risk_tool_with_valid_confirmation_is_allowed():
    decision = authorize_tool_call(
        ToolCall(name="synthetic_test_tool", arguments={}),
        registry=_registry(),
        granted_permissions={"test.synthetic"},
        confirmed=True,
    )

    assert decision.outcome == PipelineOutcome.ALLOWED
    assert decision.is_allowed


def test_high_risk_tool_permission_denied_even_if_confirmed():
    # Confirmation never substitutes for permission — order matters.
    decision = authorize_tool_call(
        ToolCall(name="synthetic_test_tool", arguments={}),
        registry=_registry(),
        granted_permissions=set(),
        confirmed=True,
    )

    assert decision.outcome == PipelineOutcome.PERMISSION_DENIED


def test_unregistered_tool_name_is_denied_defensively():
    # Defense in depth: even if a ToolCall somehow names an unregistered
    # tool, the pipeline never assumes it's safe.
    decision = authorize_tool_call(
        ToolCall(name="does_not_exist", arguments={}),
        registry=_registry(),
        granted_permissions={"research.read", "test.synthetic"},
    )

    assert decision.outcome == PipelineOutcome.PERMISSION_DENIED
    assert decision.registered_tool is None
