# Authorization

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how permission scopes (used both by human-facing endpoints and by agent tools) are checked and enforced.

## Scope

General backend authorization. Agent-specific permission semantics are in [07-agents/permissions.md](../07-agents/permissions.md) — this document is the shared enforcement mechanism underneath both.

## Model

Scoped permissions (e.g. `productivity.tasks.write`), checked via a shared dependency at the API layer, so the same enforcement code path serves both direct user actions and agent-initiated tool calls (see [07-agents/permissions.md](../07-agents/permissions.md)).

## Related documentation

- [Authentication](authentication.md)
- [Agent permissions](../07-agents/permissions.md)
- [Security architecture](../12-security/security-architecture.md)
