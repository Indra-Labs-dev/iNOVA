"""Minimal AI chat endpoint — proves the Flutter -> FastAPI -> AIService ->
LLMProvider -> Ollama chain end to end (see docs/16-roadmap/mvp.md §10).

Deliberately unauthenticated and stateless for Phase 0: no memory, no tools,
no Agent Router. Revisit once a real conversation/session concept exists.
"""
from fastapi import APIRouter, Depends

from app.ai.ollama_provider import OllamaError
from app.ai.service import AIService
from app.api.deps import get_ai_service
from app.core.errors import APIError
from app.schemas.ai import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, service: AIService = Depends(get_ai_service)) -> ChatResponse:
    try:
        response_text = service.chat(payload.message)
    except OllamaError as exc:
        raise APIError(502, "llm_unavailable", "The local LLM is unavailable.") from exc
    return ChatResponse(response=response_text, model=service.model_name)
