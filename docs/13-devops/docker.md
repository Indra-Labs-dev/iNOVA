# Docker

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how Docker is used for local development and deployment.

## Scope

Containerization strategy.

## Intended use

- `docker-compose` for local development: PostgreSQL, Redis, backend — Ollama runs natively on the host to access the GPU directly rather than through container GPU passthrough complexity, unless that proves necessary.
- Production: containerized backend + managed/self-hosted PostgreSQL and Redis (see [deployment.md](deployment.md)).

## Status note

No `Dockerfile`/`docker-compose.yml` exists yet — this describes target setup for when the backend exists to containerize.

## Related documentation

- [Environments](environments.md)
- [Deployment](deployment.md)
- [CI/CD](ci-cd.md)
