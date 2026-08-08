# CodeAgent

**Status:** [PLANNED] — Phase 4
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Objective

Assist with code inspection, generation, refactoring, and dependency/project analysis inside the [Programming Hub](../../08-modules/programming-hub.md).

## Responsibilities

- Inspect project structure, files, and dependencies.
- Propose code changes, generate tests, assist with debugging.
- Collaborate with `CyberAgent` on security-aware development flows (see [orchestration.md](../orchestration.md)).

## Inputs

A development intent (e.g. "analyze my API security", "add tests for module X"), plus read access to the relevant project.

## Outputs

Proposed diffs/patches, generated tests, analysis reports — always presented as **Preview → Review → Approve → Apply → Rollback** (see [programming-hub.md](../../08-modules/programming-hub.md)), never applied directly.

## Tools

- `read_project_file` — LOW risk.
- `analyze_dependencies` — LOW risk.
- `propose_code_change` — MEDIUM risk (produces a diff, does not apply it).
- `apply_code_change` — HIGH risk, REQUIRED confirmation.
- `run_tests` — MEDIUM risk, sandboxed execution.

Exact tool set to be finalized at implementation time; none currently implemented.

## Permissions

`code.read`, `code.write` (proposed scopes — `TODO — decision required` on final naming).

## Risks

MEDIUM to HIGH depending on tool — applying changes or running code are HIGH risk and sandboxed (see [sandboxing.md](../sandboxing.md)).

## Memory

Project-scoped context (recently inspected files, known dependency graph) — not global cross-project memory.

## Dependencies

[LLMProvider](../../06-ai/llm-provider.md), `CyberAgent`, Git/GitHub integration (see [programming-hub.md](../../08-modules/programming-hub.md)).

## Events

`agent.task.succeeded` / `agent.task.failed`, `code.change.proposed`.

## Errors

Malformed diff, failing tests post-change, inaccessible repository → surfaced clearly, change never silently applied.

## Confirmation

REQUIRED for `apply_code_change`; optional for read/analysis tools.

## Audit

Every proposed and applied change logged with full diff per [audit.md](../audit.md), enabling rollback.

## Related documentation

- [Programming Hub](../../08-modules/programming-hub.md)
- [Sandboxing](../sandboxing.md)
- [CyberAgent](cyber-agent.md)
