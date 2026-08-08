# Containers

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

C4-style "Container" level: the deployable/runnable units that make up iNOVA and how they talk to each other.

## Scope

Deployment-unit granularity. Internal module structure is in [components.md](components.md).

## Containers

| Container | Technology | Talks to |
|---|---|---|
| `frontend-web` | Flutter (web target) | `api-gateway` via REST + WebSocket |
| `frontend-3d` | Three.js/WebGL, embedded in `frontend-web` | Receives events from `frontend-web`, no direct backend access |
| `api-gateway` | FastAPI | `postgres`, `redis`, `ai-core`, `agent-runtime`, `object-storage` |
| `ai-core` | Python module within `api-gateway` process (MVP) | `llm-provider` |
| `agent-runtime` | Python module within `api-gateway` process (MVP) | `llm-provider`, `postgres` (audit), tool implementations |
| `llm-provider` | Ollama (local process/service) | Model weights on local disk |
| `postgres` | PostgreSQL | — |
| `redis` | Redis | Used for pub/sub events and caching |
| `object-storage` | Local disk (dev) / S3-compatible (prod) | — |

## Deployment note

At MVP scale, `ai-core` and `agent-runtime` run **inside** the `api-gateway` process rather than as separate services — splitting them out is a later optimization, not a day-one requirement (see [product-philosophy.md](../00-overview/product-philosophy.md): avoid speculative infrastructure). This should be revisited once agent workloads are heavy enough to justify independent scaling — track that decision as a future ADR if/when it happens.

## Related documentation

- [Architecture overview](overview.md)
- [Components](components.md)
- [DevOps environments](../13-devops/environments.md)
