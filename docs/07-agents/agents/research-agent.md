# ResearchAgent

**Status:** [TESTED] — implemented (Gate 2), backend unit/integration/security-tested, verified live end to end (real Ollama, real RSS, real PostgreSQL audit). Not yet [STABLE] (no track record over time).
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

## Tools — Gate 2 scope

Only **`read_rss_feed`** is implemented, restricted to a server-side `feed_id` allowlist (never a URL — see [12-security/network-security.md](../../12-security/network-security.md) "SSRF prevention"). `search_public_source` and `fetch_document` remain `[PLANNED]` — each implies a real external API/general fetch capability, which is a new dependency decision not made in Gate 2 (see [16-roadmap/mvp.md](../../16-roadmap/mvp.md): don't build beyond the documented vertical slice).

## Permissions

`research.read` — finalized (was `TODO` in earlier drafts). Every authenticated user implicitly holds this scope in Gate 2 (no per-user grant table yet — see [09-backend/authentication.md](../../09-backend/authentication.md) open decisions); the check itself (`app/tools/pipeline.py::authorize_tool_call`) is real and server-side regardless, and is proven to block execution when the scope is absent (see `backend/tests/test_research_agent.py::test_permission_denied_blocks_execution_end_to_end`).

## Risks

LOW overall — read-only, public-source access only. No permission to write user data or execute code. Implemented tool (`read_rss_feed`) carries `Risk: LOW`, `Confirmation: not required`, matching this fiche exactly.

## Memory

Session-scoped only, as documented — no persistence across requests. `AIService.generate()` takes a single message per call; no multi-turn history is threaded through `ResearchAgent`.

## Dependencies

[LLMProvider](../../06-ai/llm-provider.md) (now supports `tools`/`system`, see [ADR-0012](../../adr/0012-tool-calling-contract.md)), [Tool Registry](../tools.md) ([ADR-0013](../../adr/0013-static-tool-registry.md)), [AuditLog](../audit.md).

## Events

`[PLANNED]` — not wired to the shared event bus yet (see [02-architecture/event-flow.md](../../02-architecture/event-flow.md)); Gate 2 uses direct audit persistence instead, which covers the same "was this action recorded" need without the event bus dependency.

## Errors

Source unreachable, timeout, invalid RSS, or HTTP error → `read_rss_feed` returns a bounded, non-crashing failure (see `backend/app/tools/research_tools.py`), recorded as `AuditOutcome.EXECUTION_FAILED`, never silently substituted with an unverified answer.

## Confirmation

Not required for `read_rss_feed` (LOW risk) — confirmed correct by the fiche. The generic confirmation-gate mechanism (`app/tools/pipeline.py`) is implemented and proven with a synthetic MEDIUM/HIGH test-only tool (never registered in production) — see [ADR-0012](../../adr/0012-tool-calling-contract.md) and `backend/tests/test_authorization_pipeline.py`.

## Audit

Implemented — every attempt (success, permission denied, invalid tool call, invalid arguments, execution failure) is written to `audit_logs`, verified both in automated tests and against a real PostgreSQL instance during live E2E verification. A genuine "no tool needed" plain-text answer is deliberately NOT audited (it isn't a permissioned action) — see [audit.md](../audit.md).

## Related documentation

- [Agent architecture](../architecture.md)
- [Research & Intelligence Hub](../../08-modules/research-hub.md)
- [Scraping policy](../../11-intelligence/scraping-policy.md)
- [ADR-0012: Tool-calling contract](../../adr/0012-tool-calling-contract.md)
- [ADR-0013: Static Tool Registry](../../adr/0013-static-tool-registry.md)
