"""ResearchAgent against a REAL Ollama instance (RSS fetch mocked, so this
test isn't also at the mercy of a live external site's uptime — the fully
real chain, including a live feed, is exercised manually per Gate 2 §18,
not in the automated suite).

Marked `ollama` and skipped by default — see pyproject.toml `addopts` and
docs/adr/0012-tool-calling-contract.md.
"""
import uuid

import httpx
import pytest
import respx

from app.agents.research_agent import ResearchAgent
from app.ai.ollama_provider import OllamaProvider
from app.ai.service import AIService
from app.core.config import get_settings
from app.models.audit_log import AuditOutcome
from app.repositories.audit_log_repository import AuditLogRepository
from app.tools.registry import RegisteredTool, ToolRegistry
from app.tools.research_tools import READ_RSS_FEED, RSS_ALLOWLIST, read_rss_feed_handler

settings = get_settings()

VALID_RSS = b"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>Python Insider</title>
<item><title>Python 3.14 released</title><link>https://blog.python.org/1</link><pubDate>Mon, 01 Jan 2026 00:00:00 GMT</pubDate></item>
</channel></rss>"""


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


def _registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(RegisteredTool(definition=READ_RSS_FEED, handler=read_rss_feed_handler))
    return registry


@respx.mock
def test_research_agent_end_to_end_against_real_ollama(db_session):
    # Only the RSS URL is mocked. The catch-all pass_through() MUST be
    # registered after the specific mock (respx matches in registration
    # order) so the real request to Ollama passes through untouched — which
    # is the whole point of this test.
    respx.get(RSS_ALLOWLIST["python_blog"]).mock(return_value=httpx.Response(200, content=VALID_RSS))
    respx.route().pass_through()

    agent = ResearchAgent(
        AIService(OllamaProvider()),
        _registry(),
        AuditLogRepository(db_session),
    )

    result = agent.research(
        "Give me the latest items from the python_blog RSS feed.", user_id=uuid.uuid4()
    )

    # Per docs/adr/0012's measured 100% reliability on this exact scenario
    # (explicit tool + clear context), this must resolve to a real tool call
    # and a synthesized answer — not a fallback message.
    assert result.outcome == AuditOutcome.SUCCESS.value, f"got answer instead: {result.answer!r}"
    assert len(result.sources) > 0
    assert result.audit_id is not None
