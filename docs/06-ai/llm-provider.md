# LLMProvider

**Status:** [PARTIAL] — `generate(message, tools?)` implemented and tool-calling-tested (Gate 1); `stream`/`embed`/`capabilities` still [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Specify the contract every model backend must satisfy, so AI Core and agents never depend on a specific provider's API shape.

## Scope

Interface contract only. Concrete implementations documented separately ([ollama.md](ollama.md)). Tool-calling reliability findings are in [ADR-0012](../adr/0012-tool-calling-contract.md).

## Why this exists

The product vision requires supporting multiple AI providers and explicitly forbids hard-coding around one (see [00-overview/objectives.md](../00-overview/objectives.md), Objective 2). The current local-only setup (4GB VRAM, [model-strategy.md](model-strategy.md)) makes this abstraction more important, not less: it is the mechanism that lets the project upgrade to a bigger local model or a cloud provider later **without rewriting agents**. See [adr/0006-llmprovider-abstraction.md](../adr/0006-llmprovider-abstraction.md).

## Implemented interface (`backend/app/ai/provider.py`)

```python
class LLMProvider(ABC):
    def generate(self, message: str, tools: list[ToolDefinition] | None = None) -> LLMResponse:
        ...
```

`LLMResponse = { content: str | None, tool_call: ToolCall | None }` — exactly one of the two is populated (see `backend/app/ai/types.py`). A `tool_call` in the response is a **proposal only**: nothing in this contract carries any authority — see [07-agents/permissions.md](../07-agents/permissions.md) and [ADR-0012](../adr/0012-tool-calling-contract.md)'s security boundary section. The caller must validate a proposal against the real tool registry before any execution.

`ToolDefinition` carries `name`, `description`, `input_schema` (JSON Schema), plus `permission`, `risk`, `confirmation_required` fields per [07-agents/permissions.md](../07-agents/permissions.md) — declared here so a provider can pass them to the model, but no permission *system* (grants, registry storage) is implemented yet.

Still `[PLANNED]`, not yet needed: `stream(messages, tools?)`, `embed(text)`, `capabilities()`, and multi-turn `messages` history (the current `generate` takes a single `message: str`, per [16-roadmap/mvp.md](../16-roadmap/mvp.md) — no conversation memory yet).

## Rule

No agent or AI Core code should import an Ollama-specific or provider-specific client directly — only through this interface. Violating this is the single most likely way the project accidentally locks itself into the local-only setup permanently. Tool-call **text parsing** (markdown fence stripping, JSON shape) lives in `app/ai/tool_call_parsing.py`, used by `OllamaProvider` — this is provider-specific behavior and must not leak into `AIService` or any agent code.

## Related documentation

- [Architecture](architecture.md)
- [Ollama](ollama.md)
- [Tool use](tool-use.md)
- [Model strategy](model-strategy.md)
- [ADR-0012: Tool-calling contract](../adr/0012-tool-calling-contract.md)
