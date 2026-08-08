# Environments

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the environment tiers iNOVA runs in.

## Scope

Environment definitions. Local setup steps are in [local-development.md](local-development.md).

## Tiers

| Environment | Purpose | LLM backend |
|---|---|---|
| Local development | Day-to-day coding | Ollama on developer's own GPU (4GB VRAM baseline — see [06-ai/model-strategy.md](../06-ai/model-strategy.md)) |
| Staging | Pre-release verification | `TODO — decision required` — likely same Ollama setup initially |
| Production | Live for real users | `TODO — decision required` — depends on whether local-only remains viable at real user load |

## Related documentation

- [Local development](local-development.md)
- [Deployment](deployment.md)
- [Docker](docker.md)
