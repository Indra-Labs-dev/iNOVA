"""Conversation endpoints — see docs/06-ai/memory.md and
docs/09-backend/api-design.md.

Thin router: all orchestration lives in ConversationService, all
persistence/scoping in ConversationRepository/MessageRepository (see
docs/09-backend/architecture.md layer rules). `current_user` is resolved
server-side from the JWT; a conversation_id in the URL is always
re-validated against the authenticated user (get_for_user) before any read
or write — a client can never reach another user's conversation, whether
or not it guesses a valid id (see tests/test_conversations_api.py).
"""
import uuid

from fastapi import APIRouter, Depends

from app.ai.ollama_provider import OllamaError
from app.api.deps import (
    get_conversation_repository,
    get_conversation_service,
    get_current_user,
    get_message_repository,
)
from app.core.errors import APIError
from app.models.conversation import Conversation
from app.models.user import User
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.conversations import (
    ConversationResponse,
    MessageResponse,
    SendMessageRequest,
    SendMessageResponse,
)
from app.services.conversation_service import ConversationService

router = APIRouter()


def _get_owned_conversation(
    conversation_id: str, user: User, repo: ConversationRepository
) -> Conversation:
    try:
        parsed_id = uuid.UUID(conversation_id)
    except ValueError:
        raise APIError(404, "conversation_not_found", "No such conversation.") from None

    conversation = repo.get_for_user(parsed_id, user.id)
    if conversation is None:
        # Same response whether the id doesn't exist or belongs to someone
        # else — never confirm another user's conversation exists.
        raise APIError(404, "conversation_not_found", "No such conversation.")
    return conversation


@router.post("", response_model=ConversationResponse, status_code=201)
def create_conversation(
    current_user: User = Depends(get_current_user),
    repo: ConversationRepository = Depends(get_conversation_repository),
) -> ConversationResponse:
    conversation = repo.create(user_id=current_user.id)
    return ConversationResponse(
        id=str(conversation.id), created_at=conversation.created_at, updated_at=conversation.updated_at
    )


@router.get("", response_model=list[ConversationResponse])
def list_conversations(
    current_user: User = Depends(get_current_user),
    repo: ConversationRepository = Depends(get_conversation_repository),
) -> list[ConversationResponse]:
    conversations = repo.list_for_user(current_user.id)
    return [
        ConversationResponse(id=str(c.id), created_at=c.created_at, updated_at=c.updated_at)
        for c in conversations
    ]


@router.post("/{conversation_id}/messages", response_model=SendMessageResponse)
def send_message(
    conversation_id: str,
    payload: SendMessageRequest,
    current_user: User = Depends(get_current_user),
    repo: ConversationRepository = Depends(get_conversation_repository),
    service: ConversationService = Depends(get_conversation_service),
) -> SendMessageResponse:
    conversation = _get_owned_conversation(conversation_id, current_user, repo)

    try:
        turn = service.send_message(conversation.id, payload.content)
    except OllamaError as exc:
        raise APIError(502, "llm_unavailable", "The local LLM is unavailable.") from exc

    repo.touch(conversation)

    return SendMessageResponse(
        user_message=MessageResponse(
            id=str(turn.user_message.id),
            role=turn.user_message.role,
            content=turn.user_message.content,
            created_at=turn.user_message.created_at,
        ),
        assistant_message=MessageResponse(
            id=str(turn.assistant_message.id),
            role=turn.assistant_message.role,
            content=turn.assistant_message.content,
            created_at=turn.assistant_message.created_at,
        ),
    )


@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
def list_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    repo: ConversationRepository = Depends(get_conversation_repository),
    message_repo: MessageRepository = Depends(get_message_repository),
) -> list[MessageResponse]:
    conversation = _get_owned_conversation(conversation_id, current_user, repo)
    messages = message_repo.list_for_conversation(conversation.id)
    return [
        MessageResponse(id=str(m.id), role=m.role, content=m.content, created_at=m.created_at)
        for m in messages
    ]


@router.delete("/{conversation_id}", status_code=204)
def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    repo: ConversationRepository = Depends(get_conversation_repository),
) -> None:
    conversation = _get_owned_conversation(conversation_id, current_user, repo)
    repo.delete(conversation)
