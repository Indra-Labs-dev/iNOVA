"""Request/response shapes for /api/v1/conversations.

`SendMessageRequest` deliberately has exactly one field. There is
structurally no `user_id` or `conversation_id` field to accept from the
client beyond the path parameter, which is always re-checked against the
authenticated user server-side (see app/api/v1/conversations.py) — see
tests/test_conversations_api.py for the isolation regression tests.
"""
from datetime import datetime

from pydantic import BaseModel, Field


class ConversationResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime


class SendMessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class SendMessageResponse(BaseModel):
    user_message: MessageResponse
    assistant_message: MessageResponse
