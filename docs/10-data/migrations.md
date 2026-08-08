# Migrations

**Status:** [PLANNED] — no migration tool configured yet
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how schema changes will be tracked once implementation starts.

## Scope

Migration process/tooling.

## Approach

`TODO — decision required`. Whichever is chosen: migrations are the only way schema changes happen — no manual production schema edits.

### Options

| Option | Pros | Cons |
|---|---|---|
| Alembic (SQLAlchemy) | De facto standard for FastAPI backends, mature, auto-generates migrations from ORM models | Ties the data layer to SQLAlchemy as the ORM |
| Raw SQL migrations (versioned `.sql` files, no ORM-tied tool) | No ORM lock-in, full control over generated SQL | No auto-generation, more manual work, more error-prone at team scale |
| A different Python ORM's native migration tool (if SQLAlchemy isn't chosen) | Consistency with whatever ORM is picked | Only relevant if the ORM choice itself is still open |

### Decision criteria

- **ORM choice**: this decision is downstream of choosing SQLAlchemy (or not) as the backend ORM — not yet decided independently, but SQLAlchemy is the default assumption implied by [09-backend/fastapi.md](../09-backend/fastapi.md) conventions.
- **Team familiarity**: Alembic is the lowest-friction default for a FastAPI-conventional stack; deviate only with a concrete reason.
- **Timing**: must be settled before the first migration is written in Phase 0, since switching tools after real migrations exist is costly.

## Related documentation

- [Database schema](database-schema.md)
- [PostgreSQL](postgresql.md)
- [Environments](../13-devops/environments.md)
