# Knowledge Graph (Data Layer)

**Status:** [PLANNED] — Future
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the data representation behind the [Knowledge Graph module](../08-modules/knowledge-graph.md).

## Scope

Data/storage concerns. Product-level description is in [08-modules/knowledge-graph.md](../08-modules/knowledge-graph.md).

## Representation

`TODO — decision required` on storage approach.

### Options

| Option | Pros | Cons |
|---|---|---|
| Relational edge-table model on existing PostgreSQL | No new infrastructure dependency, consistent with [data-architecture.md](data-architecture.md)'s minimal-dependency bias, adequate for shallow traversals | Multi-hop graph queries become increasingly awkward/slow in pure SQL as depth grows |
| PostgreSQL graph extension (e.g. Apache AGE) | Graph query language on existing PostgreSQL, no separate database to operate | Less mature/common tooling, still a new extension to operate and learn |
| Dedicated graph database (e.g. Neo4j) | Best-in-class graph traversal performance and query ergonomics | New infrastructure dependency, new operational burden, contradicts the minimal-dependency bias unless clearly justified |

### Decision criteria

- **Actual query patterns needed**: the module isn't built yet ([08-modules/knowledge-graph.md](../08-modules/knowledge-graph.md) is `Future`) — this should be decided against real query requirements once News/Research ingestion produces enough linked data to test against, not speculatively now.
- **Dependency minimalism** (see [product-philosophy.md](../00-overview/product-philosophy.md)): the relational edge-table model is the default starting assumption specifically because it avoids a new dependency; only move off it if traversal performance is measured and found insufficient.
- **Timing**: this decision is not blocking for Phase 0–5; it only needs to be made when Knowledge Graph work actually begins (Future phase).

## Related documentation

- [Knowledge Graph module](../08-modules/knowledge-graph.md)
- [Entities](entities.md)
