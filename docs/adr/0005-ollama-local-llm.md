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

## Addendum — 2026-08-08 (Phase 0 implementation)

During Phase 0 backend scaffolding, pulling the originally specified `qwen2.5:3b-instruct-q4_K_M` tag from the Ollama registry in the actual development environment measured ~200 KB/s (~2.5h for the ~1.9GB download) — impractical to block Foundation work on. The environment already had `qwen2.5-coder:3b` fully pulled (same 3.1B-parameter class, same Q4_K_M quantization, same VRAM footprint, and it advertises Ollama's `tools` capability, which is exactly what agent tool-calling needs).

**Adjustment**: the backend's default `OLLAMA_MODEL` configuration value is set to `qwen2.5-coder:3b` for this environment, not `qwen2.5:3b-instruct-q4_K_M`. This does not change the decision above (local Ollama, ~3B-class model, Q4_K_M, 4GB VRAM) — only the specific tag, driven by real network conditions rather than a re-evaluation of model choice. `qwen2.5:3b-instruct-q4_K_M` remains pullable and swappable via the `OLLAMA_MODEL` env var with no code change, per the [LLMProvider](../06-ai/llm-provider.md) abstraction — switch to it (or benchmark both) whenever bandwidth allows.
