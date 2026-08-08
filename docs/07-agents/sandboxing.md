# Sandboxing

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how HIGH-risk tool execution is isolated from the rest of the system.

## Scope

Execution isolation strategy. Permission gating (which decides *whether* to execute) is in [permissions.md](permissions.md); this document covers *how* execution is contained once approved.

## Requirement

Any tool marked `Sandbox: REQUIRED` in its permission definition (see [permissions.md](permissions.md)) must run in an isolated context — e.g. a container with constrained filesystem/network access — rather than directly in the backend process. This applies especially to [Programming Hub](../08-modules/programming-hub.md) actions like code execution or dependency installation.

## Status note

No sandboxing mechanism exists yet — this is a target requirement for when the first `HIGH` risk tool (likely in `CodeAgent` or `CyberAgent`) is implemented. Do not ship a `HIGH`-risk, sandbox-required tool without this in place.

## Related documentation

- [Permissions](permissions.md)
- [Agent security](../12-security/agent-security.md)
- [Docker](../13-devops/docker.md)
