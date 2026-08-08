# FastAPI

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Record the decision and conventions around FastAPI as the backend framework.

## Scope

Framework-specific concerns. See [adr/0004-fastapi-backend.md](../adr/0004-fastapi-backend.md) for rationale.

## Conventions

- Pydantic models for all request/response schemas — no untyped dict passing across layer boundaries.
- Dependency injection used for auth, DB sessions, and permission checks rather than ad hoc checks scattered in route handlers.
- Routers organized per domain (see [api-design.md](api-design.md)), not one giant router file.

## Related documentation

- [Architecture](architecture.md)
- [API design](api-design.md)
