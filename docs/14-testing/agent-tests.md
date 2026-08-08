# Agent Tests

**Status:** [PLANNED] — high priority once agents exist
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Verify that agent behavior actually respects the security model, not just that it "works."

## Scope

Agent execution, tool-call validation, permission enforcement, confirmation gates.

## Required coverage before any agent ships

- A malformed/invalid tool call is rejected, not executed (see [06-ai/tool-use.md](../06-ai/tool-use.md)).
- A HIGH-risk tool call without confirmation is blocked (see [07-agents/permissions.md](../07-agents/permissions.md)).
- Every executed tool call produces an audit entry (see [07-agents/audit.md](../07-agents/audit.md)).
- Given the local model's higher malformed-call rate ([06-ai/model-strategy.md](../06-ai/model-strategy.md)), tests should include adversarial/malformed inputs, not just the happy path — this is where a small local model is most likely to surface real bugs.

## Related documentation

- [Strategy](strategy.md)
- [Agent security](../12-security/agent-security.md)
- [Security tests](security-tests.md)
