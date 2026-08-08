# Ollama

**Status:** [IMPLEMENTED] — `OllamaProvider` wired up in Phase 0 backend scaffold
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Document the current concrete LLM runtime.

## Scope

Ollama-specific setup and operational notes. See [adr/0005-ollama-local-llm.md](../adr/0005-ollama-local-llm.md) for the decision rationale (including its 2026-08-08 addendum).

## Current configuration

| Parameter | Value |
|---|---|
| Runtime | Ollama |
| Hardware | GPU with ~4GB VRAM |
| Model actually configured (`OLLAMA_MODEL` default) | `qwen2.5-coder:3b` — see [ADR-0005 addendum](../adr/0005-ollama-local-llm.md#addendum--2026-08-08-phase-0-implementation): the originally documented tag was impractically slow to pull in the real dev environment (~200KB/s, ~2.5h), and `qwen2.5-coder:3b` was already available with an equivalent size/quantization/VRAM footprint and Ollama `tools` capability |
| Originally documented starting model | `qwen2.5:3b-instruct-q4_K_M` — still the target once pulled; swappable via env var, no code change |
| Fallback/upgrade model | `qwen2.5:7b-instruct-q4_K_M` (partial CPU offload expected) |

## Why Qwen2.5 at this size

Qwen2.5 is natively trained for tool-use, which matters more than raw fluency for an agent-heavy product like iNOVA. At 3B parameters (Q4 quantization) it fits entirely in 4GB VRAM. See [model-strategy.md](model-strategy.md) for the full tradeoff analysis and other candidates considered (Llama-3.2-3B, Phi-3.5-mini).

## Operational notes

- Runs as a local service; the backend (`api-gateway`) calls it over its local API, wrapped by the [LLMProvider](llm-provider.md) implementation — never called directly from agent code.
- No per-token billing; cost is electricity + development iteration time (see [iNOVA_CAHIER_DES_CHARGES.md §5.1bis](../../iNOVA_CAHIER_DES_CHARGES.md)).
- Setup steps belong in [15-development/setup.md](../15-development/setup.md) once the backend exists to configure against it.

## Tool-calling behavior (measured, Gate 1)

`qwen2.5-coder:3b` advertises `tools` in `ollama list`'s capability tag, but in practice, against this local Ollama build:

- It **never** populates Ollama's native `message.tool_calls` response field — a tool-call proposal always arrives as JSON text inside `message.content`, sometimes markdown-fenced (` ```json ... ``` `).
- It is fully reliable for a request that clearly matches the one tool offered with an explicit argument, and fully unreliable (invents a tool name) when no offered tool actually matches the request.

`OllamaProvider` accounts for both — see [ADR-0012](../adr/0012-tool-calling-contract.md) for the full experiment, data, and consequences.

## Related documentation

- [LLMProvider](llm-provider.md)
- [Tool use](tool-use.md)
- [Model strategy](model-strategy.md)
- [ADR-0005](../adr/0005-ollama-local-llm.md)
- [ADR-0012: Tool-calling contract](../adr/0012-tool-calling-contract.md)
