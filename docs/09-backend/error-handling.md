# Error Handling

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define a consistent error contract across the API.

## Scope

Backend error responses. Agent-specific failure handling is in [07-agents/agent-lifecycle.md](../07-agents/agent-lifecycle.md).

## Principles

- Never leak internal stack traces or secrets in error responses.
- Distinguish user-actionable errors (bad input, permission denied) from system errors (upstream service down) so the frontend/mascot can react appropriately (e.g. `warning` vs `error` state — see [05-mascot/state-machine.md](../05-mascot/state-machine.md)).

## Error envelope format

`TODO — decision required` on exact shape.

### Options

| Option | Pros | Cons |
|---|---|---|
| `{ error: { code, message, details } }` (nested) | Clear namespacing, room to grow (e.g. `details` for field-level validation errors), common in mature APIs | Slightly more verbose than a flat shape |
| Flat `{ code, message, details }` | Simpler to consume on the frontend | Less clean if more error metadata is added later (namespace collisions) |
| RFC 7807 "Problem Details for HTTP APIs" | Standardized, tooling-friendly, self-describing via `type` URIs | More ceremony than needed at MVP scale; `type` URIs need real documentation pages to be meaningful |

### Decision criteria

- **Frontend consumption pattern**: whichever shape is easiest to handle uniformly in the Riverpod error-state pattern ([03-frontend/state-management.md](../03-frontend/state-management.md)) should win — this should be validated against real frontend code once it exists, not decided in the abstract.
- **Consistency with FastAPI defaults**: FastAPI's built-in `HTTPException` produces a `{"detail": ...}` shape by default — the chosen envelope should either embrace or deliberately override this default consistently across all endpoints, not mix both.
- **Timing**: must be fixed before the first API endpoint ships, since changing the envelope shape later is a breaking change for the frontend.

## Related documentation

- [API design](api-design.md)
- [Agent lifecycle](../07-agents/agent-lifecycle.md)
