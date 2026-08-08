# Entities

**Status:** [PLANNED] — conceptual model, no schema implemented
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the conceptual entities iNOVA's data model is built from, before any schema/migration is written.

## Scope

Conceptual entity list. Relations and diagram are in [database-schema.md](database-schema.md).

## Entities

| Entity | Purpose |
|---|---|
| `User` | Account identity |
| `Session` | Auth session |
| `Conversation` | A chat thread with AI Hub |
| `Message` | A single message within a conversation |
| `Memory` | Durable, distilled facts retained across sessions (see [06-ai/memory.md](../06-ai/memory.md)) |
| `Agent` | Registered agent definition (identity, capabilities, tools) |
| `AgentExecution` | One agent run, linked to its audit trail |
| `Tool` | Registered tool definition (schema, permission, risk) |
| `Permission` | A grantable scope |
| `AuditLog` | Immutable record of a permissioned action |
| `Mission` | A user goal broken into tasks |
| `MissionTask` | One step of a mission |
| `Project` | A user's tracked project (Programming Hub) |
| `Document` | An uploaded or ingested document |
| `Source` | A news/research source (RSS feed, API, etc.) |
| `NewsItem` | One ingested, processed news item |
| `Watchlist` | A user-defined monitored topic set |
| `SecurityFinding` | A Cybersecurity/OSINT Hub result |
| `Device` | A registered user device (Device Hub) |
| `Notification` | A delivered or pending notification |
| `Achievement` | A gamification unlockable |
| `UserProgress` | XP, levels, learning progress |

## Rule

Do not add columns or entities beyond what a concrete feature requires — this list is the target conceptual model, not a license to pre-build a full schema before the corresponding module is in `[IN PROGRESS]`.

## Related documentation

- [Database schema](database-schema.md)
- [Data architecture](data-architecture.md)
- [Migrations](migrations.md)
