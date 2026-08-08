# Memory

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define what iNOVA remembers about a user across sessions, and how that's separated from raw conversation history.

## Scope

AI memory model. Database representation is in [10-data/entities.md](../10-data/entities.md).

## MVP scope

Short-term conversation memory only (current session context) — per [16-roadmap/mvp.md](../16-roadmap/mvp.md).

## Target scope (post-MVP)

- Durable memory: explicit facts/preferences the user or system decides are worth retaining across sessions, stored separately from raw message history (see [10-data/entities.md](../10-data/entities.md) `Memory` entity).
- User-visible and user-editable: personalization must respect privacy and explicit permissions (see [00-overview/objectives.md](../00-overview/objectives.md), Objective 3) — the user must be able to see and delete what iNOVA remembers.
- Memory is never a dumping ground for full conversation logs; it stores distilled, purposeful facts.

## Related documentation

- [Context management](context-management.md)
- [Data entities](../10-data/entities.md)
- [Data protection](../12-security/data-protection.md)
