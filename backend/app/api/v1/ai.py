"""Minimal AI chat endpoint — proves the Flutter -> FastAPI -> AIService ->
LLMProvider -> Ollama chain end to end (see docs/16-roadmap/mvp.md §10).

DEPRECATED (Gate 4): superseded by POST /api/v1/conversations/{id}/messages,
which is authenticated and persists history — see
docs/09-backend/api-design.md "Deprecation: /ai/chat". No caller (frontend
or otherwise) uses this route anymore as of Gate 4 — AiChatScreen was
migrated to /conversations. Kept working rather than deleted, per the
Gate 4 GO instruction not to break the Phase 0 contract unnecessarily;
`deprecated=True` below surfaces this in the OpenAPI docs.
"""
from fastapi import APIRouter, Depends

from app.ai.ollama_provider import OllamaError
from app.ai.service import AIService
from app.api.deps import get_ai_service
from app.core.errors import APIError
from app.schemas.ai import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse, deprecated=True)
def chat(payload: ChatRequest, service: AIService = Depends(get_ai_service)) -> ChatResponse:
    try:
        response_text = service.chat(payload.message)
    except OllamaError as exc:
        raise APIError(502, "llm_unavailable", "The local LLM is unavailable.") from exc
    return ChatResponse(response=response_text, model=service.model_name)
