# Mission System

**Status:** [PLANNED] — MVP subset at MVP, full multi-agent version Phase 4+
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Turn a high-level user goal into a structured, inspectable, multi-agent execution plan.

## Scope

Product-level module description. Orchestration mechanics are in [07-agents/orchestration.md](../07-agents/orchestration.md).

## MVP subset vs. full version — resolving an apparent phase conflict

[16-roadmap/mvp.md](../16-roadmap/mvp.md) lists "Missions — simple tasks, XP" as in-scope for the MVP, while this module's multi-agent orchestration (below) depends on the [Agent Router](../07-agents/agent-router.md), which is Phase 4. This is intentional, not a roadmap error — there are two distinct tiers:

- **MVP mission**: a single linear task (e.g. one `ResearchAgent` call) with a visible plan of 1 step, completion state, and XP award on success. No [Orchestration](../07-agents/orchestration.md), no Agent Router — it uses whichever single agent exists at MVP scope directly.
- **Full Mission System (Phase 4+)**: the multi-agent orchestrated version described below (the "Secure my project" example), which genuinely requires the Agent Router and multiple agents.

Do not build the full orchestration engine to satisfy the MVP requirement — the MVP mission is a deliberately thin slice of this module's final shape.

## Example (full version, Phase 4+)

## Example

User: *"Secure my project."*

```text
MISSION
 |
+-- Analyze code
+-- Analyze dependencies
+-- Security checks
+-- Tests
+-- Proposed fixes
+-- Verification
+-- Report
```

## Requirements

The user must be able to inspect at any time: plan, current step, involved agent, tools used, results, pending confirmations, errors, final report.

## Dependencies

Full version: [Agent Router](../07-agents/agent-router.md), [Orchestration](../07-agents/orchestration.md). Both tiers: [Gamification](gamification.md) (XP on completion).

## Security considerations

Multi-agent missions do not bypass per-tool permission checks — see [07-agents/permissions.md](../07-agents/permissions.md).

## Related documentation

- [Orchestration](../07-agents/orchestration.md)
- [User journeys](../01-product/user-journeys.md)
