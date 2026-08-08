# Audit Logging

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the infrastructure-level audit logging requirement underneath agent-specific audit trails.

## Scope

General audit logging. Agent-specific trail content is in [07-agents/audit.md](../07-agents/audit.md).

## Requirement

Every permissioned action (agent tool call, sensitive user action like data deletion, permission grant/revoke) produces an immutable `AuditLog` entry (see [10-data/entities.md](../10-data/entities.md)) — stored in PostgreSQL, not just application logs which can rotate away.

## Related documentation

- [Agent audit](../07-agents/audit.md)
- [Entities](../10-data/entities.md)
