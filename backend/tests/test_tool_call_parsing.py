"""Unit tests for parse_tool_response — no network involved.

Several inputs here are the ACTUAL raw strings produced by qwen2.5-coder:3b
during the Gate 1 tool-calling experiment (docs/adr/0012-tool-calling-contract.md),
not synthetic examples — this pins down real observed behavior as a
regression test, not a hypothetical one.
"""
from app.ai.tool_call_parsing import ToolCallOutcome, parse_tool_response
from app.ai.types import ToolDefinition

RSS_TOOL = ToolDefinition(
    name="read_rss_feed",
    description="Fetch an allowed RSS feed and return recent items.",
    input_schema={
        "type": "object",
        "properties": {"feed": {"type": "string"}},
        "required": ["feed"],
    },
    permission="research.read",
    risk="LOW",
)


def test_no_tools_offered_is_always_no_tool_call():
    result = parse_tool_response("anything at all, even {\"name\": \"x\"}", offered_tools=[])
    assert result.outcome == ToolCallOutcome.NO_TOOL_CALL
    assert result.tool_call is None


def test_plain_prose_completion_is_no_tool_call():
    # Observed for "Hello, how are you today?" with a system prompt guiding
    # the model away from spurious tool calls.
    content = "I'm just a machine learning model, so I don't have feelings or emotions like humans do."
    result = parse_tool_response(content, offered_tools=[RSS_TOOL])
    assert result.outcome == ToolCallOutcome.NO_TOOL_CALL


def test_valid_tool_call_unfenced_json():
    content = '{"name": "read_rss_feed", "arguments": {"feed": "https://example.com/feed.xml"}}'
    result = parse_tool_response(content, offered_tools=[RSS_TOOL])
    assert result.outcome == ToolCallOutcome.VALID
    assert result.tool_call.name == "read_rss_feed"
    assert result.tool_call.arguments == {"feed": "https://example.com/feed.xml"}


def test_valid_tool_call_markdown_fenced():
    # Observed format: ```json\n{...}\n```
    content = '```json\n{\n  "name": "read_rss_feed",\n  "arguments": {\n    "feed": "https://example.com/feed.xml"\n  }\n}\n```'
    result = parse_tool_response(content, offered_tools=[RSS_TOOL])
    assert result.outcome == ToolCallOutcome.VALID
    assert result.tool_call.arguments["feed"] == "https://example.com/feed.xml"


def test_malformed_json_unquoted_value_is_rejected_not_guessed():
    # Actually observed from qwen2.5-coder:3b with a system prompt:
    # the tool name value is emitted unquoted, which is invalid JSON.
    content = '{"name": read_rss_feed, "arguments": {"feed": "https://example.com/feed.xml"}}'
    result = parse_tool_response(content, offered_tools=[RSS_TOOL])
    assert result.outcome == ToolCallOutcome.MALFORMED
    assert result.tool_call is None
    assert result.reason is not None


def test_malformed_missing_arguments_key():
    content = '{"name": "read_rss_feed"}'
    result = parse_tool_response(content, offered_tools=[RSS_TOOL])
    assert result.outcome == ToolCallOutcome.MALFORMED


def test_hallucinated_tool_name_is_rejected():
    # Actually observed for "What is 12 times 7?" when only read_rss_feed
    # was offered — the model invented a tool it was never given.
    content = '{"name": "calculate", "arguments": {"operation": "multiply", "num1": 12, "num2": 7}}'
    result = parse_tool_response(content, offered_tools=[RSS_TOOL])
    assert result.outcome == ToolCallOutcome.UNKNOWN_TOOL
    assert result.tool_call is None
    assert "calculate" in result.reason


def test_invalid_arguments_missing_required_field():
    content = '{"name": "read_rss_feed", "arguments": {}}'
    result = parse_tool_response(content, offered_tools=[RSS_TOOL])
    assert result.outcome == ToolCallOutcome.INVALID_ARGUMENTS
    assert "feed" in result.reason


def test_invalid_arguments_wrong_type():
    content = '{"name": "read_rss_feed", "arguments": {"feed": 12345}}'
    result = parse_tool_response(content, offered_tools=[RSS_TOOL])
    assert result.outcome == ToolCallOutcome.INVALID_ARGUMENTS


def test_arguments_not_an_object_is_invalid():
    content = '{"name": "read_rss_feed", "arguments": "https://example.com/feed.xml"}'
    result = parse_tool_response(content, offered_tools=[RSS_TOOL])
    assert result.outcome == ToolCallOutcome.INVALID_ARGUMENTS


def test_normal_completion_with_tools_offered_but_unused():
    # Observed for "What is the capital of France?" with tools offered:
    # the model answered in plain text rather than forcing a tool call.
    content = "The capital of France is Paris."
    result = parse_tool_response(content, offered_tools=[RSS_TOOL])
    assert result.outcome == ToolCallOutcome.NO_TOOL_CALL
    assert result.tool_call is None
