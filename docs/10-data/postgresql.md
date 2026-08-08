# PostgreSQL

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Record PostgreSQL's role as the primary datastore.

## Scope

Database-specific concerns. Entity definitions are in [entities.md](entities.md).

## Role

Single source of truth for all normalized domain data (see [data-architecture.md](data-architecture.md)). No business-critical data lives only in Redis or in-memory.

## Related documentation

- [Data architecture](data-architecture.md)
- [Migrations](migrations.md)
- [Backups](../13-devops/backups.md)
