# Research & Intelligence Hub

**Status:** [PLANNED] — Phase 5
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Collect, process, and synthesize information from permitted public sources.

## Scope

Product-level module description. Ingestion mechanics are in [11-intelligence/ingestion.md](../11-intelligence/ingestion.md).

## Capabilities

- Ingestion from official APIs, RSS, permitted public web pages, public documentation/datasets, and user-uploaded documents.
- AI-assisted synthesis via [ResearchAgent](../07-agents/agents/research-agent.md).

## Boundaries

Must respect robots.txt, terms of service, rate limits, copyright, authentication requirements, and source attribution. No anti-bot or access-control bypass — ever. See [scraping-policy.md](../11-intelligence/scraping-policy.md).

## Dependencies

[ResearchAgent](../07-agents/agents/research-agent.md), [ingestion pipeline](../11-intelligence/ingestion.md).

## Security considerations

Source authenticity and attribution are treated as a security/trust property, not just a UX nicety — see [source-attribution.md](../11-intelligence/source-attribution.md).

## Related documentation

- [ResearchAgent](../07-agents/agents/research-agent.md)
- [Ingestion](../11-intelligence/ingestion.md)
- [News Intelligence](news-intelligence.md)
