# News Intelligence

**Status:** [PARTIAL] — extractive digest implemented and tested (Gate 5); AI summarization explicitly deferred, see [ADR-0014](../adr/0014-defer-ai-summarization.md)
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08 (Gate 5 — Extractive News Digest)

## Purpose

Turn raw news sources into a personalized, trustworthy, source-attributed digest.

## Scope

Product-level module description. Pipeline mechanics are in [11-intelligence/](../11-intelligence/ingestion.md) and [02-architecture/data-flow.md](../02-architecture/data-flow.md).

## MVP subset vs. full version

[16-roadmap/mvp.md](../16-roadmap/mvp.md) includes basic RSS/API ingestion with AI summarization as part of the MVP — this is intentional (see [16-roadmap/phases.md](../16-roadmap/phases.md) "How MVP relates to these phases"), not a conflict with the "Phase 5" label below. The MVP slice skips deduplication, classification, source cross-checking, and personalization; the full pipeline (all stages below) is Phase 5.

**Gate 5 amendment**: AI summarization, though named in mvp.md's tree, was measured against the real local model before implementation and found unreliable at a level incompatible with the product's own trust requirement (see [ADR-0014](../adr/0014-defer-ai-summarization.md) — 0/9 on the required fact/inference distinction, plus one confirmed factual inversion). It is deferred, not shipped, pending a model-strategy change and a fresh, independent measurement. This is a measured result, not a permanent design position.

## Implementation status (Gate 5)

| Stage | Status |
|---|---|
| RSS ingestion | IMPLEMENTED / TESTED |
| Normalization (HTML-stripped, entity-unescaped, source's own text) | IMPLEMENTED / TESTED |
| Persistence (idempotent by URL) | IMPLEMENTED / TESTED |
| Attribution / source traceability | IMPLEMENTED / TESTED |
| AI summarization | DEFERRED — model reliability insufficient (see [ADR-0014](../adr/0014-defer-ai-summarization.md)) |
| Classification | PLANNED (Phase 5) |
| Semantic deduplication | PLANNED (Phase 5) — not to be confused with the idempotent-by-URL persistence constraint above, which is a data-integrity mechanism, not this pipeline stage |
| Source cross-checking | PLANNED (Phase 5) |
| Personalization | PLANNED (Phase 5) |

`POST /api/v1/news/refresh` and `GET /api/v1/news` (both authenticated, see [09-backend/api-design.md](../09-backend/api-design.md)) are the Gate 5 API surface. `backend/app/services/news_service.py` is the pipeline; `Source` rows are server-seeded only, never client-writable.

## Pipeline

Target (full, Phase 5): `Sources → Collection → Normalization → Deduplication → Classification → AI summarization → Source cross-checking → Personalization → iNOVA News Feed`

Gate 5 (implemented): `Sources → Collection → Normalization → Persistence → Feed` — see "Implementation status" above for exactly which stages exist today.

## Categories

AI, cybersecurity, programming, technology, startups, science, gaming, local news, economy, user-defined topics.

## Requirements

- Every item retains source link and publication date — **implemented**.
- AI summaries clearly distinguish source facts, inference, opinion, and uncertainty — **not yet applicable**: no AI summary is produced (see "Gate 5 amendment" above); the digest shows the source's own text instead, which trivially satisfies this requirement by not introducing any AI-generated claim in the first place.
- Personalized digest example: *"iNOVA Morning Intelligence"* with per-category counts and a contextual recommendation — target scope, Phase 5 (requires classification + personalization, both `PLANNED`).

## Dependencies

RSS feeds, optional news APIs (see [11-intelligence/apis.md](../11-intelligence/apis.md)). [AI Hub](ai-hub.md) for summarization is a target dependency, not a current one — `NewsService` has no dependency on `AIService`/`LLMProvider` at all as of Gate 5 (see [ADR-0014](../adr/0014-defer-ai-summarization.md)).

## Security considerations

Source attribution prevents misattributed claims; see [source-attribution.md](../11-intelligence/source-attribution.md).

## Related documentation

- [Ingestion](../11-intelligence/ingestion.md)
- [Watchlists](watchlists.md)
- [iNOVA Pulse](nova-pulse.md)
