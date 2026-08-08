# Normalization

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how heterogeneous source formats (RSS, API JSON, documents) become one consistent internal representation.

## Scope

Post-collection, pre-deduplication transformation step.

## Target shape

`TODO — decision required` on the exact normalized schema; conceptually maps to the `NewsItem`/`Document` entities in [10-data/entities.md](../10-data/entities.md) — title, body, source, published_at, url, category (raw, pre-classification).

## Related documentation

- [Ingestion](ingestion.md)
- [Deduplication](deduplication.md)
