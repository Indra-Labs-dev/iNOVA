# Agent Permissions

**Status:** [TESTED] — `authorize_tool_call` implemented and exercised by ResearchAgent (Gate 2)
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the permission model every agent tool call must pass through. This is one of the most important documents in the whole set — see also [adr/0007-agent-permissions.md](../adr/0007-agent-permissions.md) and [12-security/agent-security.md](../12-security/agent-security.md).

## Implemented (Gate 2)

`backend/app/tools/pipeline.py::authorize_tool_call(tool_call, registry, granted_permissions, confirmed)` — reads permission/risk/confirmation exclusively from the `ToolDefinition` resolved via the registry, never from the model's proposal (see [ADR-0012](../adr/0012-tool-calling-contract.md) — a `ToolCall` structurally has only `name` and `arguments`, there is no field for the model to smuggle a claimed permission or risk into). Proven to actually block execution, not just return an unused verdict — see `backend/tests/test_research_agent.py::test_permission_denied_blocks_execution_end_to_end` and the confirmation-gate tests below.

## Scope

Permission model for agent tools specifically. General backend authorization is in [09-backend/authorization.md](../09-backend/authorization.md).

## Model

Every tool declares:

```text
Tool: <name>
Permission: <scope, e.g. productivity.tasks.write>
Risk: LOW | MEDIUM | HIGH
Confirmation: optional | REQUIRED
Sandbox: not required | RECOMMENDED | REQUIRED
Audit: REQUIRED (always)
```

## Examples

```text
Tool: create_task
Permission: productivity.tasks.write
Risk: LOW
Confirmation: optional
```

```text
Tool: execute_command
Permission: system.command.execute
Risk: HIGH
Confirmation: REQUIRED
Sandbox: REQUIRED where possible
Audit: REQUIRED
```

## Non-negotiable rules

- Never execute a tool call solely because the model requested it — the permission check is independent of model output.
- HIGH-risk tools always require confirmation; there is no override.
- Every permission scope should be as narrow as practically possible (least privilege).

## Confirmation gate — implemented generically, tested with a synthetic tool

The mechanism handles LOW/MEDIUM/HIGH uniformly (not hardcoded to LOW). Gate 2 proved this with a synthetic, never-registered-in-production HIGH-risk test tool (`backend/tests/test_authorization_pipeline.py`), not by giving `ResearchAgent` a real dangerous capability: MEDIUM/HIGH without confirmation → `CONFIRMATION_REQUIRED` (blocked); MEDIUM/HIGH with `confirmed=True` → `ALLOWED`. `read_rss_feed` itself is LOW risk and never triggers this path.

## Related documentation

- [Tools](tools.md)
- [Sandboxing](sandboxing.md)
- [Audit](audit.md)
- [Agent security](../12-security/agent-security.md)
- [ADR-0012: Tool-calling contract](../adr/0012-tool-calling-contract.md)
