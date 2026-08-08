# Redis

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Record Redis's role: caching and the event bus, never primary storage.

## Scope

Redis-specific concerns.

## Role

- Event pub/sub backbone (see [02-architecture/event-flow.md](../02-architecture/event-flow.md)).
- Ephemeral caching (e.g. session lookups, rate-limit counters).

## Rule

Nothing that must survive a Redis flush should be stored only in Redis — it is a cache/bus, not a database (see [data-architecture.md](data-architecture.md)).

## Related documentation

- [Data architecture](data-architecture.md)
- [Event flow](../02-architecture/event-flow.md)
