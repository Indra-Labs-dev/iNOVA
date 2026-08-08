# Database Schema

**Status:** [PLANNED] — conceptual ER diagram, no migration exists
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Show how the entities in [entities.md](entities.md) relate to each other.

## Scope

Conceptual ER diagram. Actual migrations are tracked in [migrations.md](migrations.md) once they exist.

## Diagram

```mermaid
erDiagram
    USER ||--o{ SESSION : has
    USER ||--o{ CONVERSATION : owns
    CONVERSATION ||--o{ MESSAGE : contains
    USER ||--o{ MEMORY : has
    USER ||--o{ MISSION : requests
    MISSION ||--o{ MISSION_TASK : contains
    MISSION_TASK }o--|| AGENT : "executed by"
    AGENT ||--o{ AGENT_EXECUTION : produces
    AGENT_EXECUTION ||--o{ AUDIT_LOG : writes
    AGENT }o--o{ TOOL : "can use"
    TOOL ||--|| PERMISSION : requires
    USER ||--o{ PROJECT : owns
    PROJECT ||--o{ DOCUMENT : contains
    USER ||--o{ WATCHLIST : defines
    SOURCE ||--o{ NEWS_ITEM : produces
    WATCHLIST }o--o{ NEWS_ITEM : matches
    USER ||--o{ SECURITY_FINDING : "receives"
    USER ||--o{ DEVICE : registers
    USER ||--o{ NOTIFICATION : receives
    USER ||--|| USER_PROGRESS : has
    USER_PROGRESS ||--o{ ACHIEVEMENT : unlocks
```

## Note

This diagram reflects the target conceptual model from [entities.md](entities.md). It will diverge from the real schema until migrations exist — always trust `migrations.md` and the actual codebase over this diagram once implementation begins, and update this file when they do.

## Related documentation

- [Entities](entities.md)
- [Migrations](migrations.md)
