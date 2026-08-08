# Authorization (Security View)

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

State the security invariant authorization must uphold across both human and agent-initiated actions.

## Scope

Security requirements; enforcement mechanism is in [09-backend/authorization.md](../09-backend/authorization.md) and [07-agents/permissions.md](../07-agents/permissions.md).

## Invariant

**Every mutating action — whether initiated by a human via the API or by an agent via a tool call — passes through the same permission check.** There is no privileged bypass path for agents.

## Least privilege

Every permission scope should be as narrow as practically possible; a tool/endpoint should request the minimum scope it needs, never a broad "admin"-style catch-all.

## Related documentation

- [Backend authorization](../09-backend/authorization.md)
- [Agent permissions](../07-agents/permissions.md)
