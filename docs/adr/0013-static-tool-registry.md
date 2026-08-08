# ADR-0013: Static in-code Tool Registry (not DB-driven)

**Status:** Accepted
**Date:** 2026-08-08

## Context

[07-agents/tools.md](../07-agents/tools.md) requires a central registry so tools are defined once and reused across agents. [16-roadmap/mvp.md](../16-roadmap/mvp.md)'s Phase 1 plan flagged this as an open decision: a table-backed dynamic registry (tools/permissions stored in PostgreSQL, editable at runtime) vs. a static registry defined in Python code at process startup. This must be decided before building the registry that `ResearchAgent`'s `read_rss_feed` will be registered in (Gate 2).

## Decision

Static, in-code registry: each `ToolDefinition` (name, description, `input_schema`, `permission`, `risk`, `confirmation_required`) is declared as a Python object at module load time, paired with its handler function, in `app/tools/registry.py`. No database table stores tool definitions. No API endpoint can register, modify, or remove a tool.

## Rationale

| Criterion | Static (code) | Dynamic (DB) |
|---|---|---|
| Attack surface | None — a tool's permission/risk/schema cannot be changed without a code change + deploy, reviewed like any other code change | An endpoint or DB write path that can alter a tool's permission/risk is itself a security-critical surface — exactly what [12-security/agent-security.md](../12-security/agent-security.md) and this Gate's rule ("Flutter must never be able to register a tool, modify its permissions...") warn against |
| Auditability | Every tool change is a Git commit with review history | Requires its own audit trail for registry changes, on top of the audit trail for tool *executions* |
| Complexity at current scale | One tool (`read_rss_feed`) plus one synthetic test tool — trivial to hardcode | Would require admin UI/API, migrations, and validation tooling for a benefit not needed yet |
| Matches existing pattern | Consistent with [ADR-0008](0008-modular-architecture.md) (avoid speculative infrastructure) and the Phase 0 precedent of keeping the schema minimal (`docs/PROJECT_STATUS.md`: "add only tables actually needed this phase") | — |

A dynamic registry is not rejected forever — see Consequences.

## Consequences

- `Flutter` (or any API caller) has structurally no path to influence a tool's registration, permission, risk, or handler — the registry is a Python import, not a database row. This directly satisfies this Gate's requirement.
- Adding a new tool requires a code change and redeploy — acceptable at the current scale (Phase 1: one real tool), reconsider once the number of tools/agents grows enough that redeploy-per-tool becomes a real operational burden (a Phase 4+ concern, when the Agent Router and multiple agents land).
- The registry's `permission`/`risk`/`confirmation_required` fields are the single source of truth consulted by the permission-validation pipeline (see [07-agents/permissions.md](../07-agents/permissions.md)) — never re-derived from LLM output, per [ADR-0012](0012-tool-calling-contract.md).

## Alternatives considered

- DB-backed dynamic registry — deferred, not rejected; revisit if/when tool count or the need for non-developer tool configuration grows enough to justify the added attack surface and operational complexity.
