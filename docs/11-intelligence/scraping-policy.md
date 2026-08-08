# Scraping Policy

**Status:** Stable — policy document, applies regardless of implementation state
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Set a hard boundary on how iNOVA is allowed to collect data from the web.

## Scope

Applies to every ingestion path: [Research Hub](../08-modules/research-hub.md), [News Intelligence](../08-modules/news-intelligence.md), [OSINT Hub](../08-modules/osint-hub.md).

## Rules (non-negotiable)

- Official APIs and RSS are always preferred over scraping.
- robots.txt must be respected on any site iNOVA reads.
- Terms of service must be respected — no automated collection where explicitly disallowed.
- Rate limits must be respected, with backoff on 429/throttling responses.
- Every piece of collected content retains source attribution and publication date.
- Copyright is respected — iNOVA summarizes and attributes, it does not republish full copyrighted text.
- **No mechanism may be built to bypass anti-bot protection or access controls, under any circumstance.**

## Related documentation

- [Ingestion](ingestion.md)
- [Source attribution](source-attribution.md)
