# User Journeys

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Walk through representative end-to-end interactions to validate that the architecture actually supports them.

## Scope

Illustrative flows for the MVP scope (see [16-roadmap/mvp.md](../16-roadmap/mvp.md)). Detailed technical flows are in [02-architecture/data-flow.md](../02-architecture/data-flow.md).

## Journey 1 — First conversation

1. User opens iNOVA, authenticates.
2. Aira greets (`welcome` state).
3. User asks a question; AI Hub responds using [LLMProvider](../06-ai/llm-provider.md), with memory initialized.
4. Aira reflects `thinking` → `speaking` states per [05-mascot/state-machine.md](../05-mascot/state-machine.md).

## Journey 2 — Delegating to an agent

1. User asks iNOVA to research a topic.
2. [Agent Router](../07-agents/agent-router.md) selects `ResearchAgent`.
3. `ResearchAgent` uses a scoped, low-risk tool (e.g. `search_public_source`) — no confirmation required per its risk level.
4. Result returned with source attribution; audit entry recorded ([audit.md](../07-agents/audit.md)).

## Journey 3 — A mission with a confirmation gate

1. User says "Secure my project."
2. [Mission System](../08-modules/mission-system.md) builds a plan: inspect code → inspect dependencies → security checks → propose fixes.
3. `CodeAgent` and `CyberAgent` collaborate; each tool call is checked against its permission and risk level.
4. A `HIGH` risk tool (e.g. modifying a dependency file) triggers a mandatory confirmation UI before execution.
5. User reviews the mission report; XP awarded per [gamification.md](../08-modules/gamification.md).

## Journey 4 — Morning digest

1. Scheduled job runs the [News Intelligence pipeline](../08-modules/news-intelligence.md).
2. User opens iNOVA; sees a personalized digest with source-attributed summaries.
3. Aira surfaces a `incoming_event` state if a watchlist item is `CRITICAL`.

## Related documentation

- [Data flow](../02-architecture/data-flow.md)
- [Event flow](../02-architecture/event-flow.md)
- [Mission system](../08-modules/mission-system.md)
