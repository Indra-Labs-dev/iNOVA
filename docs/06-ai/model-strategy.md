# Model Strategy

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Make the hardware-driven model choice, and its consequences, explicit and revisable — not an accidental permanent limitation.

## Scope

Model selection reasoning. Runtime specifics are in [ollama.md](ollama.md).

## Current constraint

Development hardware: **4GB VRAM**. This is documented as a **current** constraint, adaptable later (more VRAM, a second machine, or a cloud provider) — never treated as a permanent ceiling on iNOVA's AI capability.

## Models evaluated for 4GB VRAM (Q4_K_M quantization)

| Model | Size in Q4 | Tool-use fit |
|---|---|---|
| Qwen2.5-3B-Instruct | ~2GB | Best fit — native tool-use training, fully fits in VRAM |
| Llama-3.2-3B-Instruct | ~2GB | Moderate — tool-use mostly via prompting |
| Phi-3.5-mini (3.8B) | ~2.2GB | Good general reasoning, weaker tool-use |
| Qwen2.5-7B-Instruct | ~4.7GB | Best quality, requires partial CPU offload (slower) |

**Decision:** start with `qwen2.5:3b-instruct-q4_K_M`; move to `qwen2.5:7b-instruct-q4_K_M` if offload latency proves acceptable during development.

## Consequences to design around

- Multi-step agentic tool-calling ([07-agents/](../07-agents/architecture.md)) will be **less reliable** than with a frontier cloud model — expect malformed or hallucinated tool calls more often.
- All tool calls must be strictly validated server-side (JSON schema), never trusted (see [12-security/agent-security.md](../12-security/agent-security.md)).
- MVP agent chains should stay short (1–2 tools per task) rather than long autonomous reasoning chains (see [16-roadmap/mvp.md](../16-roadmap/mvp.md)).
- The [LLMProvider](llm-provider.md) abstraction must stay real in the code, so upgrading hardware or adding a cloud provider later doesn't require rewriting agents.

## Related documentation

- [LLMProvider](llm-provider.md)
- [Ollama](ollama.md)
- [Agent security](../12-security/agent-security.md)
- [Cahier des charges §5.1bis](../../iNOVA_CAHIER_DES_CHARGES.md)
