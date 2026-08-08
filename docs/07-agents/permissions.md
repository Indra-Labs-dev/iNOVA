# Agent Permissions

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the permission model every agent tool call must pass through. This is one of the most important documents in the whole set — see also [adr/0007-agent-permissions.md](../adr/0007-agent-permissions.md) and [12-security/agent-security.md](../12-security/agent-security.md).

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

## Related documentation

- [Tools](tools.md)
- [Sandboxing](sandboxing.md)
- [Audit](audit.md)
- [Agent security](../12-security/agent-security.md)
