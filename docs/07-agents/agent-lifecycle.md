# Agent Lifecycle

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the states an agent execution moves through, end to end.

## Scope

Single execution lifecycle. Long-lived agent registration/versioning is out of scope until agents reach `[IN PROGRESS]`.

## Lifecycle

```text
User request
   |
Agent decision (routed by Agent Router)
   |
Tool selected
   |
Permission check
   |
Confirmation (if required by risk level)
   |
Execution
   |
Result
   |
Audit log
```

Each step maps to a concrete document: [agent-router.md](agent-router.md), [tools.md](tools.md), [permissions.md](permissions.md), [audit.md](audit.md).

## Failure handling

A failure at any step (invalid tool call, denied permission, user rejects confirmation, execution error) must terminate the step cleanly, report a clear status to the user, and still write an audit entry — silent failures are not acceptable (see [audit.md](audit.md)).

## Related documentation

- [Architecture](architecture.md)
- [Agent router](agent-router.md)
- [Audit](audit.md)
