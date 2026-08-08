# Mission System

**Status:** [PARTIAL] — MVP subset implemented (Gate 3): single-goal, single-step mission via `ResearchAgent`, server-computed XP on success. Full multi-agent version remains `[PLANNED]`, Phase 4+.
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08 (Gate 3 — Mission System MVP)

## Purpose

Turn a high-level user goal into a structured, inspectable, multi-agent execution plan.

## Scope

Product-level module description. Orchestration mechanics are in [07-agents/orchestration.md](../07-agents/orchestration.md).

## MVP subset vs. full version — resolving an apparent phase conflict

[16-roadmap/mvp.md](../16-roadmap/mvp.md) lists "Missions — simple tasks, XP" as in-scope for the MVP, while this module's multi-agent orchestration (below) depends on the [Agent Router](../07-agents/agent-router.md), which is Phase 4. This is intentional, not a roadmap error — there are two distinct tiers:

- **MVP mission**: a single linear task (e.g. one `ResearchAgent` call) with a visible plan of 1 step, completion state, and XP award on success. No [Orchestration](../07-agents/orchestration.md), no Agent Router — it uses whichever single agent exists at MVP scope directly.
- **Full Mission System (Phase 4+)**: the multi-agent orchestrated version described below (the "Secure my project" example), which genuinely requires the Agent Router and multiple agents.

Do not build the full orchestration engine to satisfy the MVP requirement — the MVP mission is a deliberately thin slice of this module's final shape.

## MVP implementation (Gate 3, implemented)

`POST /api/v1/missions` — see [api-design.md](../09-backend/api-design.md). `MissionService` (`backend/app/services/mission_service.py`) wraps `ResearchAgent.research()` as a black box: it adds no AI/tool/permission logic of its own, only interprets the already-validated, already-audited result.

- `Mission` (`backend/app/models/mission.py`): one row per mission, `status` (`completed`/`failed` — `pending`/`running` are conceptual only since execution is synchronous at this Gate), `failure_reason` preserving `ResearchAgent`'s real outcome verbatim (e.g. `permission_denied`, `invalid_tool_call`) rather than a generic failure message, `xp_awarded`.
- XP is awarded via `UserProgressRepository.add_xp()` — additive-only, server-side, on `AuditOutcome.SUCCESS` only. The client cannot supply or influence `xp_awarded`; `MissionRequest` has exactly one field (`goal`).
- No `MissionTask` table, no Agent Router, no queue — single synchronous step.
- Frontend: `features/missions/` renders "Mission complete +X XP" (X always from the server response) or the real failure reason, no gamification UI (no leaderboard/achievements/levels/streaks/badges).

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
