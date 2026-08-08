"""Real integration test: AIService -> OllamaProvider -> real Ollama.

Marked `ollama` and excluded from the default test run (see pyproject.toml
`addopts`) — this suite must never require a running Ollama instance to be
green. Run explicitly with:

    .venv/bin/python -m pytest -m ollama -v

Skips cleanly (not a failure) if Ollama isn't reachable, per
docs/14-testing/agent-tests.md: "can be explicitly marked as local/
integration and must not make the whole suite depend on the model."
"""
import httpx
import pytest

from app.ai.ollama_provider import OllamaProvider
from app.ai.service import AIService
from app.ai.types import ToolDefinition
from app.core.config import get_settings

settings = get_settings()

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


def _ollama_reachable() -> bool:
    try:
        httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=3)
        return True
    except httpx.HTTPError:
        return False


pytestmark = [
    pytest.mark.ollama,
    pytest.mark.skipif(not _ollama_reachable(), reason="Ollama not reachable at settings.ollama_base_url"),
]


def _service() -> AIService:
    return AIService(OllamaProvider())


def test_plain_completion_against_real_ollama():
    result = _service().chat("Reply with exactly: Gate 1 integration check OK.")
    assert isinstance(result, str)
    assert len(result) > 0


def test_tool_call_against_real_ollama_with_explicit_feed_url():
    response = _service().generate(
        "Give me the latest items from this RSS feed: https://example.com/feed.xml",
        tools=[RSS_TOOL],
    )
    # Documented, measured behavior (docs/adr/0012): qwen2.5-coder:3b was
    # 100% reliable on this exact scenario (explicit tool + explicit URL)
    # across repeated real-Ollama trials during the Gate 1 experiment.
    assert response.is_tool_call, f"expected a tool call, got content={response.content!r}"
    assert response.tool_call.name == "read_rss_feed"
    assert "feed" in response.tool_call.arguments


def test_unrelated_prompt_never_executes_a_real_tool_even_if_model_hallucinates():
    # Security-boundary regression test, not a "does the model behave" test:
    # regardless of what the model proposes for an out-of-scope prompt, the
    # result must never be a valid call to a tool it wasn't offered.
    response = _service().generate("What is 12 times 7?", tools=[RSS_TOOL])
    if response.is_tool_call:
        assert response.tool_call.name == "read_rss_feed"
