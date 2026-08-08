# Tools

**Status:** [TESTED] — `ToolRegistry` implemented (Gate 2), one real tool registered (`read_rss_feed`)
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define what a "tool" is structurally, distinct from the permission model wrapped around it.

## Scope

Tool definition contract. Permission enforcement is in [permissions.md](permissions.md); the model-facing calling contract is in [06-ai/tool-use.md](../06-ai/tool-use.md).

## Tool definition — implemented

`ToolDefinition` (`backend/app/ai/types.py`): `{ name, description, input_schema (JSON Schema), permission, risk, confirmation_required }`. A `RegisteredTool` (`backend/app/tools/registry.py`) pairs a `ToolDefinition` with its backend-owned `handler` function.

## Registry — static, in-code (decided)

Tools are registered centrally in `ToolRegistry` (`backend/app/tools/registry.py`), a static Python object populated at import time — **not** a database table. See [ADR-0013](../adr/0013-static-tool-registry.md) for the full rationale: no API endpoint can register, modify, or remove a tool, its permission, or its risk level. `default_registry` is the process-wide singleton; `app/tools/research_tools.py` registers `read_rss_feed` into it at import time.

## Allowlisting

Each agent only sees the subset of the registry it's allowed to use — implemented via `ToolRegistry.definitions_for_permissions(granted_permissions)`, used by `ResearchAgent` before every call to the model (see [agents/research-agent.md](agents/research-agent.md)). There is no global "all tools available" mode for any agent.

## Related documentation

- [Permissions](permissions.md)
- [Tool use (AI-facing contract)](../06-ai/tool-use.md)
- [Agent architecture](architecture.md)
- [ADR-0013: Static Tool Registry](../adr/0013-static-tool-registry.md)
