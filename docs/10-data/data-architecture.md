# Data Architecture

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

State the top-level principle governing how iNOVA's data is modeled.

## Scope

Cross-cutting data principles. Concrete entities are in [entities.md](entities.md); schema/relations in [database-schema.md](database-schema.md).

## Principle

Separate, normalized domain models — never one giant "user data" table. The system separates: identity, user preferences, conversations, AI memory, agent executions, tools, permissions, tasks, news, sources, documents, security findings, projects, audit logs.

## Storage split

| Data kind | Store | Detail |
|---|---|---|
| Structured domain data | PostgreSQL | [postgresql.md](postgresql.md) |
| Cache, event bus, ephemeral state | Redis | [redis.md](redis.md) |
| Files, media, 3D assets | Object storage | [object-storage.md](object-storage.md) |

## Related documentation

- [Entities](entities.md)
- [Database schema](database-schema.md)
- [Data protection](../12-security/data-protection.md)
