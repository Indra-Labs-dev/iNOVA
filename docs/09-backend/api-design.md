# API Design

**Status:** [PLANNED] — no endpoint implemented yet
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Document the intended API surface so implementation follows one consistent shape instead of ad hoc endpoints per feature.

## Scope

Endpoint inventory and conventions. Auth mechanics are in [authentication.md](authentication.md).

## Planned endpoint groups

```text
/api/v1/auth
/api/v1/users
/api/v1/ai
/api/v1/agents
/api/v1/tools
/api/v1/missions
/api/v1/news
/api/v1/research
/api/v1/security
/api/v1/projects
/api/v1/devices
/api/v1/notifications
```

**Status: PLANNED for all groups above.** Do not create these routes in code before the corresponding module is actually being implemented — this list is a target map, not a scaffolding instruction.

## Conventions (to apply once implementation starts)

- Versioned from day one (`/api/v1/...`).
- Consistent error envelope (see [error-handling.md](error-handling.md)).
- Every mutating endpoint enforces the same permission model used by agents (see [07-agents/permissions.md](../07-agents/permissions.md)) — humans and agents go through the same authorization path.

## Related documentation

- [Architecture](architecture.md)
- [Authentication](authentication.md)
- [Authorization](authorization.md)
