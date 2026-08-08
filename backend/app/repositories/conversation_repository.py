"""Data access for Conversation — see docs/06-ai/memory.md.

Every read/write is scoped by user_id — this is the enforcement point for
"no user can access another user's conversation" (see
docs/12-security/data-protection.md, docs/12-security/authorization.md).
No orchestration logic here — ConversationService decides what to do;
this only persists/scopes it.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session as DbSession

from app.models.conversation import Conversation


class ConversationRepository:
    def __init__(self, db: DbSession):
        self._db = db

    def create(self, *, user_id: uuid.UUID) -> Conversation:
        conversation = Conversation(user_id=user_id)
        self._db.add(conversation)
        self._db.commit()
        self._db.refresh(conversation)
        return conversation

    def get_for_user(self, conversation_id: uuid.UUID, user_id: uuid.UUID) -> Conversation | None:
        return (
            self._db.query(Conversation)
            .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
            .one_or_none()
        )

    def list_for_user(self, user_id: uuid.UUID, limit: int = 50) -> list[Conversation]:
        return (
            self._db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .all()
        )

    def touch(self, conversation: Conversation) -> None:
        conversation.updated_at = datetime.now(timezone.utc)
        self._db.add(conversation)
        self._db.commit()

    def delete(self, conversation: Conversation) -> None:
        self._db.delete(conversation)
        self._db.commit()
