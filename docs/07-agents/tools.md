# Tools

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define what a "tool" is structurally, distinct from the permission model wrapped around it.

## Scope

Tool definition contract. Permission enforcement is in [permissions.md](permissions.md); the model-facing calling contract is in [06-ai/tool-use.md](../06-ai/tool-use.md).

## Tool definition

A tool is a named, schema-validated capability: `{ name, description, parameters (JSON schema), permission scope, risk level }`. Tools are registered centrally (a "Tool Registry," see [02-architecture/components.md](../02-architecture/components.md)) so the same tool can be reused by multiple agents without duplication.

## Allowlisting

Each agent only sees the subset of the registry it's allowed to use (see individual agent fiches starting at [research-agent.md](agents/research-agent.md)) — there is no global "all tools available" mode for any agent.

## Related documentation

- [Permissions](permissions.md)
- [Tool use (AI-facing contract)](../06-ai/tool-use.md)
- [Agent architecture](architecture.md)
