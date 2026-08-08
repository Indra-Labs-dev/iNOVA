"""OllamaProvider tests — HTTP mocked via respx, no real Ollama/GPU needed
(see docs/14-testing/agent-tests.md). Tool-call parsing edge cases live in
test_tool_call_parsing.py; this file covers OllamaProvider's own plumbing
(request shape, error handling, delegation to the parser)."""
import httpx
import pytest
import respx

from app.ai.ollama_provider import OllamaError, OllamaProvider
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


@respx.mock
def test_generate_returns_plain_completion_when_no_tools_offered():
    respx.post("http://fake-ollama:11434/api/chat").mock(
        return_value=httpx.Response(200, json={"message": {"content": "hi there"}})
    )
    provider = OllamaProvider(base_url="http://fake-ollama:11434", model="test-model")

    result = provider.generate("hello")

    assert result.content == "hi there"
    assert result.tool_call is None


@respx.mock
def test_generate_does_not_send_tools_key_when_none_offered():
    route = respx.post("http://fake-ollama:11434/api/chat").mock(
        return_value=httpx.Response(200, json={"message": {"content": "hi"}})
    )
    provider = OllamaProvider(base_url="http://fake-ollama:11434", model="test-model")

    provider.generate("hello")

    sent_body = route.calls[0].request.content
    assert b'"tools"' not in sent_body


@respx.mock
def test_generate_sends_tool_schema_and_parses_valid_tool_call():
    route = respx.post("http://fake-ollama:11434/api/chat").mock(
        return_value=httpx.Response(
            200,
            json={"message": {"content": '{"name": "read_rss_feed", "arguments": {"feed": "https://example.com/feed.xml"}}'}},
        )
    )
    provider = OllamaProvider(base_url="http://fake-ollama:11434", model="test-model")

    result = provider.generate("give me the feed", tools=[RSS_TOOL])

    sent_body = route.calls[0].request.content
    assert b'"tools"' in sent_body
    assert b"read_rss_feed" in sent_body
    assert result.is_tool_call
    assert result.tool_call.name == "read_rss_feed"
    assert result.tool_call.arguments == {"feed": "https://example.com/feed.xml"}


@respx.mock
def test_generate_falls_back_to_content_on_unknown_tool_name():
    respx.post("http://fake-ollama:11434/api/chat").mock(
        return_value=httpx.Response(200, json={"message": {"content": '{"name": "calculate", "arguments": {}}'}})
    )
    provider = OllamaProvider(base_url="http://fake-ollama:11434", model="test-model")

    result = provider.generate("what is 2+2", tools=[RSS_TOOL])

    assert result.tool_call is None
    assert result.content == '{"name": "calculate", "arguments": {}}'


@respx.mock
def test_generate_raises_on_http_error():
    respx.post("http://fake-ollama:11434/api/chat").mock(return_value=httpx.Response(500))
    provider = OllamaProvider(base_url="http://fake-ollama:11434", model="test-model")

    with pytest.raises(OllamaError):
        provider.generate("hello")


@respx.mock
def test_generate_raises_on_unexpected_response_shape():
    respx.post("http://fake-ollama:11434/api/chat").mock(return_value=httpx.Response(200, json={"unexpected": True}))
    provider = OllamaProvider(base_url="http://fake-ollama:11434", model="test-model")

    with pytest.raises(OllamaError):
        provider.generate("hello")
