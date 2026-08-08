# Classification

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Assign each ingested item to a category and relevance signal.

## Scope

Post-deduplication, pre-summarization step.

## Categories

AI, cybersecurity, programming, technology, startups, science, gaming, local news, economy, user-defined topics — per [News Intelligence](../08-modules/news-intelligence.md).

## Approach

`TODO — decision required` — likely a lightweight classification pass using the local LLM ([06-ai/model-strategy.md](../06-ai/model-strategy.md)) or simpler keyword/source-based rules at MVP scale, given the reliability tradeoffs of small local models.

## Related documentation

- [Ingestion](ingestion.md)
- [Watchlists](../08-modules/watchlists.md)
