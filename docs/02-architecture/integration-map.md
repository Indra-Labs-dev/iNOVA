# Integration Map

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Single reference of every external integration point, its purpose, and its documentation.

## Scope

External systems only — internal module-to-module wiring is in [components.md](components.md) and [event-flow.md](event-flow.md).

| Integration | Purpose | Required for | Detail |
|---|---|---|---|
| Ollama (local) | LLM inference | AI Hub, all agents | [06-ai/ollama.md](../06-ai/ollama.md) |
| Cloud LLM provider (optional) | Fallback/upgrade inference path | Future, if local proves insufficient | [06-ai/llm-provider.md](../06-ai/llm-provider.md) |
| RSS feeds | News ingestion | News Intelligence | [11-intelligence/rss.md](../11-intelligence/rss.md) |
| CVE/NVD API | Vulnerability data | Cybersecurity Hub | [08-modules/cybersecurity-hub.md](../08-modules/cybersecurity-hub.md) |
| GitHub API | Repo/PR integration | Programming Hub | [08-modules/programming-hub.md](../08-modules/programming-hub.md) |
| Object storage (S3-compatible) | Assets, uploads, GLTF/GLB | 3D world, documents | [10-data/object-storage.md](../10-data/object-storage.md) |
| Email provider | Account verification, alerts | Auth, notifications | [09-backend/authentication.md](../09-backend/authentication.md) |
| PostgreSQL | Primary datastore | Everything | [10-data/postgresql.md](../10-data/postgresql.md) |
| Redis | Cache + event bus | Everything | [10-data/redis.md](../10-data/redis.md) |

## Related documentation

- [System context](system-context.md)
- [Cahier des charges — dépendances externes](../../iNOVA_CAHIER_DES_CHARGES.md)
