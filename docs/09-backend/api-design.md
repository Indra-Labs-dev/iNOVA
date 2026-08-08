# API Design

**Status:** [PARTIAL] — `/auth`, `/ai`, `/agents/research` implemented; the rest remain `[PLANNED]`
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Document the intended API surface so implementation follows one consistent shape instead of ad hoc endpoints per feature.

## Scope

Endpoint inventory and conventions. Auth mechanics are in [authentication.md](authentication.md).

## Endpoint groups

```text
/api/v1/auth       — IMPLEMENTED (register, login, refresh, logout, me)
/api/v1/ai         — IMPLEMENTED (chat — Phase 0, unauthenticated, no tools)
/api/v1/agents     — PARTIAL (POST /agents/research only — Gate 2, ResearchAgent)
/api/v1/users      — PLANNED
/api/v1/tools      — PLANNED (no endpoint exposes the Tool Registry — see docs/adr/0013-static-tool-registry.md: it must stay backend-only, not become an API surface)
/api/v1/missions   — PLANNED
/api/v1/news       — PLANNED
/api/v1/research   — PLANNED (superseded in scope by /agents/research for Phase 1 — reconcile naming when the full Research Hub is built, Phase 5)
/api/v1/security   — PLANNED
/api/v1/projects   — PLANNED
/api/v1/devices    — PLANNED
/api/v1/notifications — PLANNED
```

Do not create the remaining routes in code before the corresponding module is actually being implemented — this list is a target map, not a scaffolding instruction.

## `POST /api/v1/agents/research` (implemented, Gate 2)

Requires authentication (unlike `/ai/chat` — this endpoint performs permissioned, audited actions, so "who" must be real). Request: `{query: string, confirmed?: boolean}`. Response: `{answer: string, sources: [{title, link, published}], audit_id: string | null, outcome: string}`. See [ResearchAgent](../07-agents/agents/research-agent.md) for the orchestration behind it; the router itself (`backend/app/api/v1/agents.py`) contains no business logic, per the convention below.

## Conventions

- Versioned from day one (`/api/v1/...`) — followed.
- Consistent error envelope (see [error-handling.md](error-handling.md)) — followed.
- Every mutating/permissioned endpoint enforces the same permission model used by agents (see [07-agents/permissions.md](../07-agents/permissions.md)) — followed for `/agents/research`; humans and agents go through the same `authorize_tool_call` path.
- Routers stay thin; orchestration lives in services/agents, not route handlers — followed (`app/api/v1/agents.py` is ~15 lines).

## Related documentation

- [Architecture](architecture.md)
- [Authentication](authentication.md)
- [Authorization](authorization.md)
- [ResearchAgent](../07-agents/agents/research-agent.md)
