# Orchestration

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how multiple agents collaborate on a single mission.

## Scope

Multi-agent coordination for [Mission System](../08-modules/mission-system.md) use cases. Single-agent routing is in [agent-router.md](agent-router.md).

## Example (target behavior, not yet built)

```text
"Secure my project"
   |
CodeAgent -> inspect project, dependencies, relevant code
   |
CyberAgent -> security analysis, vulnerability classification, recommendations
   |
CodeAgent -> propose fixes, generate tests
   |
Human review -> verify changes
```

## Rule

Agent collaboration does not bypass per-tool permission checks — each agent in the chain still passes through [permissions.md](permissions.md) independently for its own tool calls. High-impact actions require explicit authorization regardless of how many agents are involved.

## Related documentation

- [Agent router](agent-router.md)
- [Mission System](../08-modules/mission-system.md)
- [Permissions](permissions.md)
