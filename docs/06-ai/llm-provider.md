# LLMProvider

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Specify the contract every model backend must satisfy, so AI Core and agents never depend on a specific provider's API shape.

## Scope

Interface contract only. Concrete implementations documented separately ([ollama.md](ollama.md)).

## Why this exists

The product vision requires supporting multiple AI providers and explicitly forbids hard-coding around one (see [00-overview/objectives.md](../00-overview/objectives.md), Objective 2). The current local-only setup (4GB VRAM, [model-strategy.md](model-strategy.md)) makes this abstraction more important, not less: it is the mechanism that lets the project upgrade to a bigger local model or a cloud provider later **without rewriting agents**. See [adr/0006-llmprovider-abstraction.md](../adr/0006-llmprovider-abstraction.md).

## Conceptual interface

```text
LLMProvider
├── generate(messages, tools?) -> completion | tool_call
├── stream(messages, tools?) -> token stream
├── embed(text) -> vector          # if/when retrieval needs it
└── capabilities() -> { supports_tool_use, context_window, ... }
```

`[PLANNED]` — exact method signatures to be finalized when `ai-core` implementation begins; this is the target contract, not shipped code.

## Rule

No agent or AI Core code should import an Ollama-specific or provider-specific client directly — only through this interface. Violating this is the single most likely way the project accidentally locks itself into the local-only setup permanently.

## Related documentation

- [Architecture](architecture.md)
- [Ollama](ollama.md)
- [Model strategy](model-strategy.md)
