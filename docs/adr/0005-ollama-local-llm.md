# ADR-0005: Ollama / local LLM for current development

**Status:** Accepted — explicitly revisable
**Date:** 2026-08-08

## Context

AI Core ([06-ai/](../06-ai/architecture.md)) needs an LLM backend. Available development hardware has ~4GB VRAM. A cloud LLM API would remove hardware constraints but introduces per-token cost and an external dependency from day one.

## Decision

Use Ollama running locally as the current LLM backend, starting with `qwen2.5:3b-instruct-q4_K_M` (see [06-ai/model-strategy.md](../06-ai/model-strategy.md) for the full model comparison).

## Consequences

- No per-token billing; cost is electricity and development iteration time (see [iNOVA_CAHIER_DES_CHARGES.md §5.1bis](../../iNOVA_CAHIER_DES_CHARGES.md)).
- Lower tool-calling reliability than a frontier cloud model — this is treated as an active design constraint across [07-agents/](../07-agents/architecture.md) (short tool chains, strict server-side validation), not ignored.
- This decision is explicitly a **current, revisable constraint**, not a permanent architectural commitment — see [ADR-0006](0006-llmprovider-abstraction.md), which is what makes reversing this decision cheap later.

## Alternatives considered

- Cloud LLM API (Claude, OpenAI, etc.) — better tool-calling reliability and no hardware constraint, but introduces recurring cost and an external dependency; deferred, not rejected — remains available behind the `LLMProvider` interface if local proves insufficient.
