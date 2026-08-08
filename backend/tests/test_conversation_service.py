"""ConversationService orchestration tests — AIService is faked (no LLM, no
network), mirroring test_mission_service.py. This suite is about
ConversationService's own logic (history bounding, write ordering, error
behavior), not AIService's or OllamaProvider's, which are covered elsewhere.
"""
import uuid

import pytest

from app.ai.types import LLMResponse
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.services.conversation_service import ConversationService


class FakeAIService:
    def __init__(self, response: LLMResponse | None = None, error: Exception | None = None):
        self._response = response or LLMResponse(content="Hi there!", tool_call=None)
        self._error = error
        self.calls: list[dict] = []

    def generate(self, message, tools=None, system=None, history=None):
        self.calls.append({"message": message, "system": system, "history": history})
        if self._error:
            raise self._error
        return self._response


def _conversation(db_session):
    return ConversationRepository(db_session).create(user_id=uuid.uuid4())


def test_send_message_persists_user_and_assistant_turns(db_session):
    conversation = _conversation(db_session)
    ai_service = FakeAIService(LLMResponse(content="I can help with that.", tool_call=None))
    message_repo = MessageRepository(db_session)
    service = ConversationService(ai_service, message_repo, history_window=10)

    turn = service.send_message(conversation.id, "I'm working on iNOVA.")

    assert turn.user_message.role == "user"
    assert turn.user_message.content == "I'm working on iNOVA."
    assert turn.assistant_message.role == "assistant"
    assert turn.assistant_message.content == "I can help with that."

    stored = message_repo.list_for_conversation(conversation.id)
    assert [m.content for m in stored] == ["I'm working on iNOVA.", "I can help with that."]


def test_send_message_passes_bounded_prior_history_not_including_current_message(db_session):
    conversation = _conversation(db_session)
    message_repo = MessageRepository(db_session)
    message_repo.add(conversation_id=conversation.id, role="user", content="turn 1")
    message_repo.add(conversation_id=conversation.id, role="assistant", content="reply 1")

    ai_service = FakeAIService()
    service = ConversationService(ai_service, message_repo, history_window=10)

    service.send_message(conversation.id, "turn 2")

    assert ai_service.calls[0]["message"] == "turn 2"
    assert ai_service.calls[0]["history"] == [
        {"role": "user", "content": "turn 1"},
        {"role": "assistant", "content": "reply 1"},
    ]


def test_send_message_bounds_history_to_the_configured_window(db_session):
    conversation = _conversation(db_session)
    message_repo = MessageRepository(db_session)
    for i in range(6):
        message_repo.add(conversation_id=conversation.id, role="user", content=f"msg-{i}")

    ai_service = FakeAIService()
    service = ConversationService(ai_service, message_repo, history_window=2)

    service.send_message(conversation.id, "current")

    assert ai_service.calls[0]["history"] == [
        {"role": "user", "content": "msg-4"},
        {"role": "user", "content": "msg-5"},
    ]


def test_send_message_persists_nothing_when_the_llm_call_fails(db_session):
    conversation = _conversation(db_session)
    message_repo = MessageRepository(db_session)
    ai_service = FakeAIService(error=RuntimeError("Ollama unreachable"))
    service = ConversationService(ai_service, message_repo, history_window=10)

    with pytest.raises(RuntimeError):
        service.send_message(conversation.id, "hello")

    assert message_repo.list_for_conversation(conversation.id) == []
