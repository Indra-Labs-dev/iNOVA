# Memory

**Status:** [PARTIAL] — short-term (session) memory implemented and tested (Gate 4); durable cross-session memory still `[PLANNED]`
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08 (Gate 4 — Conversation & Short-Term Memory)

## Purpose

Define what iNOVA remembers about a user across sessions, and how that's separated from raw conversation history.

## Scope

AI memory model. Database representation is in [10-data/entities.md](../10-data/entities.md).

## MVP scope

Short-term conversation memory only (current session context) — per [16-roadmap/mvp.md](../16-roadmap/mvp.md).

## Implemented (Gate 4, Option A)

`Conversation` + `Message` (`backend/app/models/`), `ConversationService` (`backend/app/services/conversation_service.py`), `POST/GET /api/v1/conversations`, `POST/GET .../messages`, `DELETE /api/v1/conversations/{id}` — see [09-backend/api-design.md](../09-backend/api-design.md) and [context-management.md](context-management.md) for the bounded-window mechanism and the experiment that set its default.

This is raw, unsummarized history scoped to one conversation — not the durable, distilled `Memory` entity described below, which remains explicitly out of scope. Gate 4's own GO instructions were explicit: *"souvenir durable entre conversations n'est PAS requis dans Gate 4."* Nothing in this Gate extracts facts, builds a profile, or persists anything beyond the conversation's own message history.

## Target scope (post-MVP)

- Durable memory: explicit facts/preferences the user or system decides are worth retaining across sessions, stored separately from raw message history (see [10-data/entities.md](../10-data/entities.md) `Memory` entity).
- User-visible and user-editable: personalization must respect privacy and explicit permissions (see [00-overview/objectives.md](../00-overview/objectives.md), Objective 3) — the user must be able to see and delete what iNOVA remembers.
- Memory is never a dumping ground for full conversation logs; it stores distilled, purposeful facts.

## Related documentation

- [Context management](context-management.md)
- [Data entities](../10-data/entities.md)
- [Data protection](../12-security/data-protection.md)
