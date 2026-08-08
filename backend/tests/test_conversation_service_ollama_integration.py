"""ConversationService against a REAL Ollama instance — no HTTP to mock,
unlike ResearchAgent/MissionService, since Conversation has no tools/RSS.

Also exercises the finding from the Gate 4.4 experiment
(docs/06-ai/context-management.md "Chosen window"): a fact stated early in
a bounded-window-sized history is correctly recalled when the window
covers it.

Marked `ollama` and skipped by default — see pyproject.toml `addopts`.
"""
import uuid

import httpx
import pytest

from app.ai.ollama_provider import OllamaProvider
from app.ai.service import AIService
from app.core.config import get_settings
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.services.conversation_service import ConversationService

settings = get_settings()


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


def test_conversation_service_end_to_end_against_real_ollama(db_session):
    conversation = ConversationRepository(db_session).create(user_id=uuid.uuid4())
    service = ConversationService(
        AIService(OllamaProvider()),
        MessageRepository(db_session),
        history_window=settings.conversation_history_window,
    )

    first_turn = service.send_message(conversation.id, "I'm working on a project called Nebula-7.")
    assert first_turn.assistant_message.content

    second_turn = service.send_message(conversation.id, "What's the name of my project again?")

    assert "nebula-7" in second_turn.assistant_message.content.lower(), (
        f"expected the model to recall the project name from the bounded history, "
        f"got: {second_turn.assistant_message.content!r}"
    )
