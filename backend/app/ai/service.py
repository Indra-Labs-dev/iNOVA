"""AIService — the only entry point features/API routes use to talk to AI Core.

Depends on the LLMProvider abstraction, never a concrete provider (see
docs/06-ai/llm-provider.md). Phase 0 has no memory, no tool use, no Agent
Router — see docs/16-roadmap/mvp.md for what's deliberately deferred.
"""
from app.ai.provider import LLMProvider


class AIService:
    def __init__(self, provider: LLMProvider):
        self._provider = provider

    def chat(self, message: str) -> str:
        return self._provider.generate(message)

    @property
    def model_name(self) -> str:
        return getattr(self._provider, "model", self._provider.__class__.__name__)
