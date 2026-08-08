# ADR-0007: Explicit agent permission model

**Status:** Accepted
**Date:** 2026-08-08

## Context

iNOVA's agents ([07-agents/](../07-agents/architecture.md)) can call tools with real-world side effects. The product vision explicitly states an agent must never gain unrestricted system access, and AI output must never be treated as a safe command by default.

## Decision

Every tool declares an explicit permission scope, risk level (LOW/MEDIUM/HIGH), and confirmation requirement ([07-agents/permissions.md](../07-agents/permissions.md)). Every tool call is validated server-side before execution, regardless of what the model requested.

## Consequences

- HIGH-risk actions cannot execute without user confirmation, by construction, not by convention.
- Every action produces an audit trail ([07-agents/audit.md](../07-agents/audit.md)), enabling post-hoc review.
- Adds implementation overhead to every new tool (schema, permission scope, risk classification) — a deliberate cost given [12-security/agent-security.md](../12-security/agent-security.md).
- Particularly important given the local model's higher rate of malformed/hallucinated tool calls ([06-ai/model-strategy.md](../06-ai/model-strategy.md)) — this model was not designed only for a hypothetical future frontier model.

## Alternatives considered

- Trusting model output with lightweight prompt-based safety instructions only — rejected outright; prompting is not a security boundary.
- Coarse-grained, per-agent (rather than per-tool) permissions — rejected as insufficiently granular for least-privilege.
