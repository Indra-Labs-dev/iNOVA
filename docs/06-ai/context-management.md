# Context Management

**Status:** [TESTED] — bounded-history assembly implemented and measured (Gate 4)
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08 (Gate 4 — Conversation & Short-Term Memory)

## Purpose

Define how prompts are assembled from conversation history, memory, and retrieved data.

## Scope

Prompt construction. Long-term persistence is in [memory.md](memory.md); external grounding is in [retrieval.md](retrieval.md).

## Constraint-driven design note

Small local models (see [model-strategy.md](model-strategy.md)) have both a smaller effective context window and lower instruction-following robustness than large cloud models. Context assembly must be **deliberately minimal** — include only what's relevant to the current turn/tool decision, rather than dumping large amounts of history and hoping the model copes.

## Planned structure

```text
System instructions (role, safety rules, available tools)
   +
Relevant memory (see memory.md)
   +
Recent conversation turns (bounded window)
   +
Retrieved context, if applicable (see retrieval.md)
```

Exact token budgets `TODO — decision required` once the chosen model's real effective context window is benchmarked on the target hardware.

## Chosen window (Gate 4, measured against real qwen2.5-coder:3b)

Two scenarios were tested: a fact stated a few turns back (well inside every candidate window) and a fact stated at the very start of a 20-message history (only inside a window of 20). Window sizes 5, 10, 20, and (follow-up) 40 were measured.

- **Latency stayed flat**, roughly 0.5–2.3s per call regardless of window size in this range (5 to 40 messages) — window size was not the latency bottleneck at this conversation scale.
- **Recall was 100% correct whenever the fact was inside the window, and 100% wrong whenever it wasn't** — windows of 5 and 10 missed a fact from the start of a 20-message history every time; a window of 20 caught it every time.
- **The model never hedged on a miss** — with the fact excluded, it didn't say "I don't have that information," it confidently answered with a plausible-but-wrong guess (the product name "iNOVA" instead of the actual project name). A too-small window doesn't just lose context, it produces confident wrong answers.

Given latency is close to free in this range and a larger window measurably prevents confident wrong answers, `conversation_history_window` defaults to **20** (`backend/app/core/config.py`) — bounded, not unlimited, and still a tunable setting, not hardcoded. Not ADR'd: reversible, single-parameter, same category as prior additive `LLMProvider` changes. See `backend/tests/test_conversation_service_ollama_integration.py` for the regression test and the Gate 4 report for full experiment output.

## Related documentation

- [Memory](memory.md)
- [Retrieval](retrieval.md)
- [Model strategy](model-strategy.md)
