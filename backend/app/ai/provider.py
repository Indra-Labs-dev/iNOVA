"""LLMProvider abstraction — see docs/06-ai/llm-provider.md and
docs/adr/0006-llmprovider-abstraction.md.

No agent or service code should depend on a concrete provider (OllamaProvider,
or any future cloud provider) directly — only on this interface. Phase 0
implements only the `generate` method; `stream`/`embed`/`capabilities` from the
documented conceptual interface are deliberately not built yet (no streaming
UI, no retrieval) — extend this interface when a real caller needs them.
"""
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, message: str) -> str:
        """Return a single completion for a single user message.

        Deliberately minimal for Phase 0: no conversation history, no tool
        use, no streaming (see docs/16-roadmap/mvp.md — memory/tools/Agent
        Router are out of scope here). Extend the signature when those land.
        """
        raise NotImplementedError
