# WriterAgent

**Status:** [PLANNED] — Future
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Objective

Generate and edit written content on behalf of the user or another agent (e.g. turning `ResearchAgent` findings into a polished summary).

## Responsibilities

- Draft, summarize, translate, and edit text.
- Preserve source attribution when writing from `ResearchAgent` output.

## Inputs

A writing intent, optionally source material/findings from another agent.

## Outputs

Drafted or edited text, presented for user review before any external use (e.g. before being sent anywhere).

## Tools

- `draft_content` — LOW risk.
- `summarize_content` — LOW risk.

## Permissions

`content.generate` — no permission to publish or send on the user's behalf; that remains a human action per [12-security/agent-security.md](../../12-security/agent-security.md).

## Risks

LOW — text generation only, no external side effects.

## Memory

Style/tone preferences may be retained if the user opts in (see [06-ai/memory.md](../../06-ai/memory.md)).

## Dependencies

[LLMProvider](../../06-ai/llm-provider.md), optionally `ResearchAgent` output.

## Events

`agent.task.succeeded/failed`.

## Errors

Ambiguous source material → ask for clarification rather than inventing content.

## Confirmation

Not required to draft; required before any hypothetical future "send/publish" tool is added.

## Audit

Draft requests logged per [audit.md](../audit.md).

## Related documentation

- [ResearchAgent](research-agent.md)
- [Agent security](../../12-security/agent-security.md)
