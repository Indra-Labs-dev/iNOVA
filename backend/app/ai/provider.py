"""LLMProvider abstraction — see docs/06-ai/llm-provider.md and
docs/adr/0006-llmprovider-abstraction.md.

No agent or service code should depend on a concrete provider (OllamaProvider,
or any future cloud provider) directly — only on this interface.
"""
from abc import ABC, abstractmethod

from app.ai.types import LLMResponse, ToolDefinition


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, message: str, tools: list[ToolDefinition] | None = None) -> LLMResponse:
        """Return a completion, or a tool-call proposal if `tools` were offered
        and the model chose to use one (see docs/06-ai/tool-use.md contract).

        Still deliberately minimal: single message, no conversation history
        (see docs/16-roadmap/mvp.md). A tool call returned here is a
        PROPOSAL ONLY — see docs/07-agents/permissions.md: the caller must
        validate it against the real tool registry/permission model before
        any execution. This method never grants authority, it only reports
        what the model said.
        """
        raise NotImplementedError
