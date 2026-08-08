# Agent Security

**Status:** [PLANNED] — priority document
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

This is the central security document for iNOVA's agent system — the mission that produced this documentation set explicitly flagged it as priority.

## Scope

Everything that constrains what an agent is allowed to do and how that's enforced. Cross-references [07-agents/permissions.md](../07-agents/permissions.md), [07-agents/sandboxing.md](../07-agents/sandboxing.md), and [07-agents/audit.md](../07-agents/audit.md) — this document is the security rationale; those are the implementation-facing specs.

## Core rule

**An AI agent must never automatically gain unrestricted access to the user's system, files, network, credentials, or external services.**

## Enforced through

- Scoped permissions per tool (see [07-agents/permissions.md](../07-agents/permissions.md)).
- Tool allowlists — an agent only sees the tools it's explicitly granted, never a global registry.
- Confirmation gates for MEDIUM/HIGH-risk actions.
- Sandboxing for execution-capable tools (see [07-agents/sandboxing.md](../07-agents/sandboxing.md)).
- Full audit logs (see [07-agents/audit.md](../07-agents/audit.md)).
- Rate limiting on tool invocation to prevent runaway agent loops.
- Clear action previews before any irreversible operation.

## Example tool security definitions

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
Sandbox: RECOMMENDED / REQUIRED depending on context
Audit: REQUIRED
```

## Never do this

- Never treat an LLM's output as a safe command by default — validate every tool call's schema server-side before considering execution (see [06-ai/tool-use.md](../06-ai/tool-use.md)).
- Never let an agent chain multiple tool calls without re-checking permissions at each step, even within one mission (see [07-agents/orchestration.md](../07-agents/orchestration.md)).
- Never skip audit logging "for simple/low-risk actions" — audit is required for every action, without exception.

## Elevated risk given current AI setup

The local model in use (`qwen2.5:3b`, ~4GB VRAM constraint — see [06-ai/model-strategy.md](../06-ai/model-strategy.md)) is more prone to malformed or hallucinated tool calls than a frontier cloud model. This makes strict server-side validation (not model-side prompting alone) load-bearing rather than defense-in-depth — a malformed call must be **structurally impossible** to execute, not just "unlikely due to good prompting."

## Related documentation

- [Threat model](threat-model.md)
- [Agent permissions](../07-agents/permissions.md)
- [Sandboxing](../07-agents/sandboxing.md)
- [Audit](../07-agents/audit.md)
- [Tool use](../06-ai/tool-use.md)
