"""ConversationService — orchestration layer on top of AIService, per
docs/06-ai/memory.md MVP scope: short-term conversation memory only (a
bounded window of the current conversation's own history), no durable
cross-conversation memory.

This is NOT a second AI implementation — it never talks to LLMProvider or
Ollama directly, only through AIService (see docs/06-ai/architecture.md).
The LLM never decides who the user is, what history to read, or what gets
persisted — it only ever returns text; this service is the sole writer of
Message rows, for both the user's and the assistant's turn.
"""
import uuid
from dataclasses import dataclass

from app.ai.service import AIService
from app.models.message import Message, MessageRole
from app.repositories.message_repository import MessageRepository

_SYSTEM_PROMPT = (
    "You are Aira, the AI companion inside iNOVA. Be concise and helpful. "
    "Use the prior conversation turns you're given to stay consistent with "
    "what the user already told you in this conversation."
)


@dataclass(frozen=True)
class ConversationTurn:
    user_message: Message
    assistant_message: Message


class ConversationService:
    def __init__(self, ai_service: AIService, message_repo: MessageRepository, history_window: int):
        self._ai_service = ai_service
        self._message_repo = message_repo
        self._history_window = history_window

    def send_message(self, conversation_id: uuid.UUID, content: str) -> ConversationTurn:
        """Calls the LLM before persisting anything: if Ollama is unreachable,
        nothing is written — the caller (API layer) surfaces the error and
        the client can simply retry, rather than leaving an orphaned user
        turn with no reply.
        """
        recent = self._message_repo.recent_for_conversation(conversation_id, limit=self._history_window)
        history = [{"role": m.role, "content": m.content} for m in recent]

        response = self._ai_service.generate(content, system=_SYSTEM_PROMPT, history=history)

        user_message = self._message_repo.add(
            conversation_id=conversation_id, role=MessageRole.USER.value, content=content
        )
        assistant_message = self._message_repo.add(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT.value,
            content=response.content or "",
        )
        return ConversationTurn(user_message=user_message, assistant_message=assistant_message)
