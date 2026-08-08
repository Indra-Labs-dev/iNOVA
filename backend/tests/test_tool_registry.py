import pytest

from app.ai.types import ToolDefinition
from app.tools.registry import RegisteredTool, ToolExecutionResult, ToolRegistry

SAMPLE = ToolDefinition(
    name="read_rss_feed",
    description="Fetch an allowed RSS feed.",
    input_schema={"type": "object", "properties": {"feed_id": {"type": "string"}}, "required": ["feed_id"]},
    permission="research.read",
    risk="LOW",
)


def _handler(args: dict) -> ToolExecutionResult:
    return ToolExecutionResult(success=True, summary="ok")


def test_register_and_get_known_tool():
    registry = ToolRegistry()
    registry.register(RegisteredTool(definition=SAMPLE, handler=_handler))

    found = registry.get("read_rss_feed")

    assert found is not None
    assert found.definition.permission == "research.read"


def test_get_unknown_tool_returns_none():
    registry = ToolRegistry()
    assert registry.get("does_not_exist") is None


def test_register_duplicate_name_raises():
    registry = ToolRegistry()
    registry.register(RegisteredTool(definition=SAMPLE, handler=_handler))

    with pytest.raises(ValueError):
        registry.register(RegisteredTool(definition=SAMPLE, handler=_handler))


def test_definitions_for_permissions_filters_by_scope():
    other = ToolDefinition(
        name="admin_tool",
        description="",
        input_schema={"type": "object", "properties": {}},
        permission="admin.write",
        risk="HIGH",
    )
    registry = ToolRegistry()
    registry.register(RegisteredTool(definition=SAMPLE, handler=_handler))
    registry.register(RegisteredTool(definition=other, handler=_handler))

    visible = registry.definitions_for_permissions({"research.read"})

    assert [d.name for d in visible] == ["read_rss_feed"]


def test_definitions_for_permissions_empty_when_no_matching_scope():
    registry = ToolRegistry()
    registry.register(RegisteredTool(definition=SAMPLE, handler=_handler))

    assert registry.definitions_for_permissions({"unrelated.scope"}) == []


def test_all_definitions_ignores_permissions():
    registry = ToolRegistry()
    registry.register(RegisteredTool(definition=SAMPLE, handler=_handler))

    assert len(registry.all_definitions()) == 1
