"""Data access for Message — see docs/06-ai/memory.md, docs/06-ai/context-management.md.

No conversation_id is ever taken on faith from a caller without first going
through ConversationRepository.get_for_user — this repository has no
notion of "user" at all, by design (see docs/09-backend/architecture.md
layer rules: authorization is the service/route layer's job, not the
repository's).
"""
import uuid

from sqlalchemy.orm import Session as DbSession

from app.models.message import Message


class MessageRepository:
    def __init__(self, db: DbSession):
        self._db = db

    def add(self, *, conversation_id: uuid.UUID, role: str, content: str) -> Message:
        message = Message(conversation_id=conversation_id, role=role, content=content)
        self._db.add(message)
        self._db.commit()
        self._db.refresh(message)
        return message

    def list_for_conversation(self, conversation_id: uuid.UUID) -> list[Message]:
        """Full history, oldest first — used by GET .../messages."""
        return (
            self._db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )

    def recent_for_conversation(self, conversation_id: uuid.UUID, limit: int) -> list[Message]:
        """Bounded window for prompt assembly: the last `limit` messages,
        returned oldest first (chronological) so callers can hand them
        straight to the model — see docs/06-ai/context-management.md.
        """
        recent_desc = (
            self._db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .all()
        )
        return list(reversed(recent_desc))
