# Ollama

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Document the current concrete LLM runtime.

## Scope

Ollama-specific setup and operational notes. See [adr/0005-ollama-local-llm.md](../adr/0005-ollama-local-llm.md) for the decision rationale.

## Current configuration

| Parameter | Value |
|---|---|
| Runtime | Ollama |
| Hardware | GPU with ~4GB VRAM |
| Starting model | `qwen2.5:3b-instruct-q4_K_M` |
| Fallback/upgrade model | `qwen2.5:7b-instruct-q4_K_M` (partial CPU offload expected) |

## Why Qwen2.5 at this size

Qwen2.5 is natively trained for tool-use, which matters more than raw fluency for an agent-heavy product like iNOVA. At 3B parameters (Q4 quantization) it fits entirely in 4GB VRAM. See [model-strategy.md](model-strategy.md) for the full tradeoff analysis and other candidates considered (Llama-3.2-3B, Phi-3.5-mini).

## Operational notes

- Runs as a local service; the backend (`api-gateway`) calls it over its local API, wrapped by the [LLMProvider](llm-provider.md) implementation — never called directly from agent code.
- No per-token billing; cost is electricity + development iteration time (see [iNOVA_CAHIER_DES_CHARGES.md §5.1bis](../../iNOVA_CAHIER_DES_CHARGES.md)).
- Setup steps belong in [15-development/setup.md](../15-development/setup.md) once the backend exists to configure against it.

## Related documentation

- [LLMProvider](llm-provider.md)
- [Model strategy](model-strategy.md)
- [ADR-0005](../adr/0005-ollama-local-llm.md)
