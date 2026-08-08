# Normalization

**Status:** [PARTIAL] — implemented for RSS (Gate 5); API/document source formats remain `[PLANNED]`
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08 (Gate 5 — Extractive News Digest)

## Purpose

Define how heterogeneous source formats (RSS, API JSON, documents) become one consistent internal representation.

## Scope

Post-collection, pre-deduplication transformation step.

## Target shape

`TODO — decision required` on the exact normalized schema once non-RSS sources exist; conceptually maps to the `NewsItem`/`Document` entities in [10-data/entities.md](../10-data/entities.md) — title, body, source, published_at, url, category (raw, pre-classification).

## Implemented shape (Gate 5, RSS only)

`NewsItem` (`backend/app/models/news_item.py`): `title`, `link`, `excerpt`, `published_at`, `source_id`. No `category` field yet — deferred with classification (Phase 5), not built speculatively ahead of it. Normalization here means: HTML tags stripped and HTML entities unescaped from the RSS `<description>` for plain-text display — never a paraphrase or summary of the content (see [summarization.md](summarization.md) for why AI-generated text isn't part of this step).

## Related documentation

- [Ingestion](ingestion.md)
- [Deduplication](deduplication.md)
