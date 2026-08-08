# API Tests

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define contract-level tests against the FastAPI surface.

## Scope

HTTP request/response behavior, per [09-backend/api-design.md](../09-backend/api-design.md).

## Priority targets once endpoints exist

Auth flows, permission enforcement (a request without the right scope must be rejected — every mutating endpoint tested for this), error envelope consistency ([09-backend/error-handling.md](../09-backend/error-handling.md)).

## Related documentation

- [Strategy](strategy.md)
- [API design](../09-backend/api-design.md)
