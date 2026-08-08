"""LLMProvider abstraction — see docs/06-ai/llm-provider.md and
docs/adr/0006-llmprovider-abstraction.md.

No agent or service code should depend on a concrete provider (OllamaProvider,
or any future cloud provider) directly — only on this interface.
"""
from abc import ABC, abstractmethod

from app.ai.types import LLMResponse, ToolDefinition


class LLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        message: str,
        tools: list[ToolDefinition] | None = None,
        system: str | None = None,
    ) -> LLMResponse:
        """Return a completion, or a tool-call proposal if `tools` were offered
        and the model chose to use one (see docs/06-ai/tool-use.md contract).

        `system` is an optional system-role instruction — added in Gate 2
        because the Gate 1 experiment (docs/adr/0012-tool-calling-contract.md)
        measured it materially reducing tool-name hallucination on
        out-of-scope requests. Still a single user message, no multi-turn
        history (see docs/16-roadmap/mvp.md).

        A tool call returned here is a PROPOSAL ONLY — see
        docs/07-agents/permissions.md: the caller must validate it against
        the real tool registry/permission model before any execution. This
        method never grants authority, it only reports what the model said.
        """
        raise NotImplementedError
