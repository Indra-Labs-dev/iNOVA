# News Intelligence

**Status:** [PLANNED] — basic slice in MVP, full pipeline Phase 5
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Turn raw news sources into a personalized, trustworthy, source-attributed digest.

## Scope

Product-level module description. Pipeline mechanics are in [11-intelligence/](../11-intelligence/ingestion.md) and [02-architecture/data-flow.md](../02-architecture/data-flow.md).

## MVP subset vs. full version

[16-roadmap/mvp.md](../16-roadmap/mvp.md) includes basic RSS/API ingestion with AI summarization as part of the MVP — this is intentional (see [16-roadmap/phases.md](../16-roadmap/phases.md) "How MVP relates to these phases"), not a conflict with the "Phase 5" label below. The MVP slice skips deduplication, classification, source cross-checking, and personalization; the full pipeline (all stages below) is Phase 5.

## Pipeline

`Sources → Collection → Normalization → Deduplication → Classification → AI summarization → Source cross-checking → Personalization → iNOVA News Feed`

## Categories

AI, cybersecurity, programming, technology, startups, science, gaming, local news, economy, user-defined topics.

## Requirements

- Every item retains source link and publication date.
- AI summaries clearly distinguish source facts, inference, opinion, and uncertainty.
- Personalized digest example: *"iNOVA Morning Intelligence"* with per-category counts and a contextual recommendation.

## Dependencies

RSS feeds, optional news APIs (see [11-intelligence/apis.md](../11-intelligence/apis.md)), [AI Hub](ai-hub.md) for summarization.

## Security considerations

Source attribution prevents misattributed claims; see [source-attribution.md](../11-intelligence/source-attribution.md).

## Related documentation

- [Ingestion](../11-intelligence/ingestion.md)
- [Watchlists](watchlists.md)
- [iNOVA Pulse](nova-pulse.md)
