# Source Attribution

**Status:** [PARTIAL] — implemented for News Intelligence's RSS items (Gate 5); the "AI-added inference" boundary is not yet applicable since no AI summarization ships yet, see [ADR-0014](../adr/0014-defer-ai-summarization.md)
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08 (Gate 5 — Extractive News Digest)

## Purpose

Guarantee every piece of AI-processed content traces back to a verifiable source.

## Scope

Applies across News Intelligence, Research Hub, and any agent output derived from ingested data.

## Requirement

Every summarized/synthesized item retains: source link, publication date, and a clear boundary between quoted/sourced fact and AI-added inference. No summary should be presentable without this attribution attached.

## Implementation (Gate 5)

Every `NewsItem` carries `link`, `published_at`, and `source_id` (resolved to the source's name in the API response) — verified in `backend/tests/test_news_api.py`. There is no AI-added content to bound against source fact yet (see [summarization.md](../11-intelligence/summarization.md)): the digest shows the source's own text, so this requirement is trivially satisfied by construction rather than by an enforced boundary — that distinction will matter once (if) AI summarization is reintroduced.

## Related documentation

- [Summarization](summarization.md)
- [Scraping policy](scraping-policy.md)
- [ResearchAgent](../07-agents/agents/research-agent.md)
