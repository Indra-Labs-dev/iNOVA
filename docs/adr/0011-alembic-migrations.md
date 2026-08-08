# ADR-0011: Database migrations — Alembic

**Status:** Accepted
**Date:** 2026-08-08

## Context

[10-data/migrations.md](../10-data/migrations.md) left the migration tool open between Alembic, raw versioned SQL files, or another ORM's native tool. Phase 0 Foundation needs this resolved before the first migration is written.

## Decision

Use Alembic, paired with SQLAlchemy as the backend ORM ([09-backend/fastapi.md](../09-backend/fastapi.md)).

## Rationale

- De facto standard for FastAPI + SQLAlchemy backends — lowest-friction default for this stack, matching the criteria in [10-data/migrations.md](../10-data/migrations.md) (versionable with Git, reproducible, FastAPI/Python-adapted, CI/CD-compatible, ready for schema evolution).
- Auto-generates migrations from ORM model changes, reducing manual SQL-writing error compared to hand-written versioned SQL files.
- No team-familiarity reason to deviate from the documented default assumption.

## Consequences

- All schema changes go through Alembic migrations — no manual production schema edits, ever.
- SQLAlchemy becomes the committed ORM choice as a consequence (Alembic depends on it for autogeneration), which is consistent with [09-backend/fastapi.md](../09-backend/fastapi.md) conventions already assumed elsewhere in the documentation.

## Alternatives considered

- Raw versioned SQL migrations — rejected: more manual work and more error-prone at team scale, with no compensating benefit given SQLAlchemy is already the assumed ORM.
- A different ORM's native migration tool — not applicable; SQLAlchemy is the ORM in use.
