# Context Management

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

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

## Related documentation

- [Memory](memory.md)
- [Retrieval](retrieval.md)
- [Model strategy](model-strategy.md)
