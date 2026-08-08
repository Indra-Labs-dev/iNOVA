"""AIService — the only entry point features/API routes use to talk to AI Core.

Depends on the LLMProvider abstraction, never a concrete provider (see
docs/06-ai/llm-provider.md). Still no memory, no Agent Router — see
docs/16-roadmap/mvp.md for what's deliberately deferred. Tool-calling
(docs/adr/0012-tool-calling-contract.md) is supported through `generate()`.
"""
from app.ai.provider import LLMProvider
from app.ai.types import LLMResponse, ToolDefinition


class AIService:
    def __init__(self, provider: LLMProvider):
        self._provider = provider

    def generate(
        self,
        message: str,
        tools: list[ToolDefinition] | None = None,
        system: str | None = None,
    ) -> LLMResponse:
        return self._provider.generate(message, tools=tools, system=system)

    def chat(self, message: str) -> str:
        return self.generate(message).content or ""

    @property
    def model_name(self) -> str:
        return getattr(self._provider, "model", self._provider.__class__.__name__)
