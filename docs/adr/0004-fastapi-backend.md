# ADR-0004: FastAPI as backend framework

**Status:** Accepted
**Date:** 2026-08-08

## Context

The backend ([09-backend/](../09-backend/architecture.md)) needs to serve a REST + WebSocket API, integrate an async-heavy AI/agent workload, and stay maintainable by a small team.

## Decision

Python + FastAPI is the backend framework, with Pydantic for schema validation.

## Consequences

- Native async support fits AI/agent workloads (streaming LLM responses, concurrent tool calls).
- Automatic OpenAPI schema generation aids API documentation ([09-backend/api-design.md](../09-backend/api-design.md)).
- Python ecosystem aligns with common AI/ML tooling (relevant for [06-ai/](../06-ai/architecture.md) integration with Ollama).
- Ties the backend team to Python; no polyglot backend services planned at this stage.

## Alternatives considered

- Node.js/Express or NestJS — would unify language with a hypothetical JS frontend, but Flutter is Dart-based anyway ([ADR-0001](0001-flutter-frontend.md)), so no such synergy exists; Python's AI ecosystem was the deciding factor.
- Django — heavier, more opinionated than needed for an API-first backend.
