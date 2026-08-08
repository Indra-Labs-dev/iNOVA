# Agent Router

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how a user's intent gets matched to the right agent(s).

## Scope

Routing logic. Multi-agent collaboration on one task is in [orchestration.md](orchestration.md).

## Diagram

```text
User
  |
iNOVA Core
  |
Agent Router
  |
+---------+---------+---------+
|         |         |         |
Cyber    Code    Research   Data
Agent    Agent     Agent     Agent
|         |         |         |
+---------+---------+---------+
          |
       Result
          |
        User
```

## Design note

At MVP scope (see [16-roadmap/mvp.md](../16-roadmap/mvp.md)), only `ResearchAgent` exists, so routing is close to a no-op. The router's contract should still be built as a real decision point (not hard-coded to one agent) so adding `CodeAgent` in Phase 4 doesn't require restructuring — this mirrors the [LLMProvider](../06-ai/llm-provider.md) abstraction principle applied to agents instead of models.

## Related documentation

- [Architecture](architecture.md)
- [Orchestration](orchestration.md)
- [Agent lifecycle](agent-lifecycle.md)
