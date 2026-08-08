# Integration Tests

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define scope for tests that exercise real dependencies (DB, Redis) but not the full stack.

## Scope

Repository/service layer against a real (test) PostgreSQL instance.

## Priority targets once code exists

Data repository correctness against [10-data/entities.md](../10-data/entities.md) schema, event bus publish/subscribe behavior ([02-architecture/event-flow.md](../02-architecture/event-flow.md)).

## Related documentation

- [Strategy](strategy.md)
- [API tests](api-tests.md)
