# Ingestion

**Status:** [PARTIAL] — Collector/Normalizer/Source Attribution implemented for RSS (Gate 5); Deduplicator (semantic)/Classifier/AI Summarizer/Personalization stages remain `[PLANNED]`, Phase 5
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08 (Gate 5 — Extractive News Digest)

## Purpose

Define the overall data collection strategy and its priority order.

## Scope

Entry point for `11-intelligence/`. Sub-documents cover each pipeline stage.

## Source priority

```text
1. Official API
2. RSS
3. Public source (permitted)
4. Scraping only where explicitly permitted
```

Never build a mechanism to bypass anti-bot protection or access controls — see [scraping-policy.md](scraping-policy.md).

## Pipeline stages

```text
Sources → Collector → Normalizer → Deduplicator → Classifier → AI Summarizer → Source Attribution → Personalization → Feed
```

Each stage is documented separately: [rss.md](rss.md), [apis.md](apis.md), [normalization.md](normalization.md), [deduplication.md](deduplication.md), [classification.md](classification.md), [summarization.md](summarization.md), [source-attribution.md](source-attribution.md), [personalization.md](personalization.md).

## Cross-cutting requirements

Rate limits, robots.txt compliance, ToS compliance, attribution, caching, error handling with retry, source freshness tracking, and clear data provenance at every stage.

## Related documentation

- [Scraping policy](scraping-policy.md)
- [News Intelligence](../08-modules/news-intelligence.md)
- [Data flow](../02-architecture/data-flow.md)
