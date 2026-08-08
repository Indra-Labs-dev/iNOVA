# ResearchAgent

**Status:** [PLANNED] — first agent scheduled for implementation (Phase 4 / MVP)
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Objective

Retrieve and synthesize information from permitted public sources on behalf of the user or another agent.

## Responsibilities

- Query permitted sources (official APIs, RSS, public documentation) per [11-intelligence/ingestion.md](../../11-intelligence/ingestion.md).
- Synthesize findings with source attribution.
- Hand off results to AI Core or another agent (e.g. `WriterAgent`) rather than acting further itself.

## Inputs

A research intent/question, optionally scoped to specific sources or a time range.

## Outputs

A synthesized answer with cited sources, distinguishing fact from inference (see [11-intelligence/source-attribution.md](../../11-intelligence/source-attribution.md)).

## Tools

- `search_public_source` — LOW risk.
- `fetch_document` — LOW risk (public URLs only).
- `read_rss_feed` — LOW risk.

Exact tool set to be finalized at implementation time; none currently implemented.

## Permissions

`research.read` (proposed scope name — `TODO — decision required` to finalize against [12-security/authorization.md](../../12-security/authorization.md) conventions once written).

## Risks

LOW overall — read-only, public-source access only. No permission to write user data or execute code.

## Memory

Session-scoped by default; no persistent memory unless explicitly promoted to [AI memory](../../06-ai/memory.md) by the user or system.

## Dependencies

[LLMProvider](../../06-ai/llm-provider.md), [Research & Intelligence Hub](../../08-modules/research-hub.md).

## Events

Publishes `agent.task.succeeded` / `agent.task.failed` (see [event-flow.md](../../02-architecture/event-flow.md)).

## Errors

Source unreachable, rate-limited, or against robots.txt → fail cleanly with a clear reason, never silently substitute an unverified answer.

## Confirmation

Not required — all tools are LOW risk, read-only, public-source.

## Audit

Every source queried and every claim's attribution logged per [audit.md](../audit.md).

## Related documentation

- [Agent architecture](../architecture.md)
- [Research & Intelligence Hub](../../08-modules/research-hub.md)
- [Scraping policy](../../11-intelligence/scraping-policy.md)
