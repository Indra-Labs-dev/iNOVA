# RSS

**Status:** [IMPLEMENTED] / [TESTED] — see docs/08-modules/news-intelligence.md (Gate 5)
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08 (Gate 5 — Extractive News Digest)

## Purpose

Define RSS as the primary, lowest-friction ingestion channel.

## Scope

RSS-specific collection concerns.

## Notes

Free, low-maintenance, and ToS-friendly by design — the preferred source type per [scraping-policy.md](scraping-policy.md).

## Implementation (Gate 5)

Two feeds seeded server-side (`backend/app/models/source.py`, seeded only by migration — see [08-modules/news-intelligence.md](../08-modules/news-intelligence.md)): `python_blog`, `github_blog` — the same two already allowlisted for `ResearchAgent`'s `read_rss_feed` tool. `NewsService` fetches with the same SSRF-safe pattern (no redirects, timeout, size cap). Category mapping is still `[PLANNED]` — classification hasn't started (Phase 5), so no source is categorized yet.

## Related documentation

- [Ingestion](ingestion.md)
- [APIs](apis.md)
