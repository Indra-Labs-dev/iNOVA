# Deduplication

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Prevent the same story from multiple sources appearing as separate feed items.

## Scope

Post-normalization step, before classification.

## Approach

`TODO — decision required` on similarity method (exact URL/title match at MVP, semantic similarity via embeddings later — coordinate with [06-ai/retrieval.md](../06-ai/retrieval.md) if embeddings are introduced, given hardware constraints in [06-ai/model-strategy.md](../06-ai/model-strategy.md)).

## Related documentation

- [Ingestion](ingestion.md)
- [Normalization](normalization.md)
- [Classification](classification.md)
