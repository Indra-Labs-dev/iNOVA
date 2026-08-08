"""MissionService against a REAL Ollama instance (RSS fetch mocked, same
rationale as test_research_agent_ollama_integration.py: isolate this test
from a live external feed's uptime while still exercising the real LLM).

Marked `ollama` and skipped by default — see pyproject.toml `addopts`.
"""
import uuid

import httpx
import pytest
import respx

from app.agents.research_agent import ResearchAgent
from app.ai.ollama_provider import OllamaProvider
from app.ai.service import AIService
from app.core.config import get_settings
from app.models.mission import MissionStatus
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.mission_repository import MissionRepository
from app.repositories.user_progress_repository import UserProgressRepository
from app.services.mission_service import MISSION_SUCCESS_XP, MissionService
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
def test_mission_service_end_to_end_against_real_ollama(db_session):
    respx.get(RSS_ALLOWLIST["python_blog"]).mock(return_value=httpx.Response(200, content=VALID_RSS))
    respx.route().pass_through()

    agent = ResearchAgent(AIService(OllamaProvider()), _registry(), AuditLogRepository(db_session))
    service = MissionService(
        agent, MissionRepository(db_session), UserProgressRepository(db_session)
    )
    user_id = uuid.uuid4()

    outcome = service.start(
        "Give me the latest items from the python_blog RSS feed.", user_id=user_id
    )

    assert outcome.mission.status == MissionStatus.COMPLETED.value, f"got answer instead: {outcome.mission.answer!r}"
    assert outcome.mission.xp_awarded == MISSION_SUCCESS_XP
    assert len(outcome.sources) > 0

    progress = UserProgressRepository(db_session).get(user_id)
    assert progress.xp == MISSION_SUCCESS_XP
