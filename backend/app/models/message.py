"""Message entity — one turn of a Conversation, see docs/06-ai/memory.md.

Raw, unsummarized: this is conversation history, not the distilled `Memory`
entity (deferred, see docs/06-ai/memory.md "Target scope (post-MVP)"). The
LLM never writes a Message directly — ConversationService is the only
writer, for both the user's and the assistant's turn (see
docs/06-ai/architecture.md: AI Core owns conversation, never trusts LLM
output blindly).
"""
import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True
    )

    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
