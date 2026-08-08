# Functional Requirements

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Enumerate what the system must do, at a testable level, per module. This is the bridge between the product vision and [14-testing/strategy.md](../14-testing/strategy.md).

## Scope

Requirements for the full target product. MVP-only subset is in [16-roadmap/mvp.md](../16-roadmap/mvp.md).

## FR conventions

Each requirement: `FR-<module>-<n>`. Status uses the standard labels from [scope.md](../00-overview/scope.md).

## AI Hub

- `FR-AI-1` [PLANNED] The system must support multi-turn conversation with contextual memory.
- `FR-AI-2` [PLANNED] The system must allow the AI to invoke a defined set of tools, validated server-side.
- `FR-AI-3` [PLANNED] The system must support swapping the underlying LLM provider without changing agent logic (see [llm-provider.md](../06-ai/llm-provider.md)).

## Agents

- `FR-AGENT-1` [PLANNED] Every agent action must pass a permission check before execution.
- `FR-AGENT-2` [PLANNED] Every HIGH-risk tool call must require explicit user confirmation before execution.
- `FR-AGENT-3` [PLANNED] Every agent execution must produce an audit log entry.

## Mission System

- `FR-MISSION-1` [PLANNED] A user-given goal must be decomposable into an inspectable, ordered task list.
- `FR-MISSION-2` [PLANNED] The user must be able to view current step, involved agent, tools used, and pending confirmations at any time.

## News Intelligence

- `FR-NEWS-1` [PLANNED] Every ingested item must retain source link and publication date.
- `FR-NEWS-2` [PLANNED] AI summaries must visually distinguish sourced facts from inference/opinion.
- `FR-NEWS-3` [PLANNED] Duplicate items from multiple sources must be deduplicated before display.

## Cybersecurity Hub

- `FR-CYBER-1` [PLANNED] The system must compute and display an aggregate security posture score.
- `FR-CYBER-2` [PLANNED] All security analysis must be restricted to systems the user owns or is authorized on.

## Mascot

- `FR-MASCOT-1` [PLANNED] The mascot must visually reflect at minimum: idle, thinking, speaking, success, error.
- `FR-MASCOT-2` [PLANNED] Mascot state transitions must be driven by application events, not hard-coded per screen.

## Full requirement set

The complete FR set mirrors the module list starting at [08-modules/ai-hub.md](../08-modules/ai-hub.md) and will be expanded as each module moves from `[PLANNED]` to `[IN PROGRESS]`. Do not pre-write detailed FRs for modules not yet scheduled — add them when the module enters an active phase, to avoid stale, unverified requirements.

## Related documentation

- [Non-functional requirements](non-functional-requirements.md)
- [Feature matrix](feature-matrix.md)
- [Testing strategy](../14-testing/strategy.md)
