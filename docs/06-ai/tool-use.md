# Tool Use

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the contract for how AI Core and agents invoke tools — the mechanism that turns "AI beyond chat" (Objective 2) into something safe.

## Scope

Tool-calling contract. Permission enforcement is documented in [07-agents/permissions.md](../07-agents/permissions.md) and [12-security/agent-security.md](../12-security/agent-security.md) — this document covers the mechanical contract only.

## Contract

1. The model receives a list of available tools with their JSON schema (name, description, parameters) — scoped to what's permitted for the current user/context, not a global list.
2. If the model requests a tool call, the backend validates it against the tool's schema **before** anything else happens.
3. An invalid or malformed tool call is rejected and logged — never partially executed, never silently corrected by guessing intent.
4. A valid tool call still passes through the permission check and confirmation gate defined in [07-agents/permissions.md](../07-agents/permissions.md) before execution.

## Reliability note

Given the current small local model ([model-strategy.md](model-strategy.md)), expect a higher rate of malformed/hallucinated tool calls than with a frontier model. Step 3 above is therefore not optional hardening — it is load-bearing for MVP correctness, not just security.

## Related documentation

- [Model strategy](model-strategy.md)
- [Agent permissions](../07-agents/permissions.md)
- [Agent security](../12-security/agent-security.md)
