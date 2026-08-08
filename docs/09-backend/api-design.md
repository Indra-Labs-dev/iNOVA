# API Design

**Status:** [PARTIAL] — `/auth`, `/ai` (deprecated), `/agents/research`, `POST /missions`, `/conversations`, `/news` implemented; the rest remain `[PLANNED]`
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08 (Gate 5 — Extractive News Digest)

## Purpose

Document the intended API surface so implementation follows one consistent shape instead of ad hoc endpoints per feature.

## Scope

Endpoint inventory and conventions. Auth mechanics are in [authentication.md](authentication.md).

## Endpoint groups

```text
/api/v1/auth       — IMPLEMENTED (register, login, refresh, logout, me)
/api/v1/ai         — DEPRECATED (chat — Phase 0, unauthenticated, no tools; superseded by /conversations, Gate 4 — see below)
/api/v1/agents     — PARTIAL (POST /agents/research only — Gate 2, ResearchAgent)
/api/v1/users      — PLANNED
/api/v1/tools      — PLANNED (no endpoint exposes the Tool Registry — see docs/adr/0013-static-tool-registry.md: it must stay backend-only, not become an API surface)
/api/v1/missions   — PARTIAL (POST /missions only — Gate 3, MVP; GET deferred)
/api/v1/conversations — IMPLEMENTED (Gate 4 — create/list, send/list messages, delete)
/api/v1/news       — PARTIAL (Gate 5 — refresh + digest; AI summarization deferred, see ADR-0014)
/api/v1/research   — PLANNED (superseded in scope by /agents/research for Phase 1 — reconcile naming when the full Research Hub is built, Phase 5)
/api/v1/security   — PLANNED
/api/v1/projects   — PLANNED
/api/v1/devices    — PLANNED
/api/v1/notifications — PLANNED
```

Do not create the remaining routes in code before the corresponding module is actually being implemented — this list is a target map, not a scaffolding instruction.

## `POST /api/v1/agents/research` (implemented, Gate 2)

Requires authentication (unlike `/ai/chat` — this endpoint performs permissioned, audited actions, so "who" must be real). Request: `{query: string, confirmed?: boolean}`. Response: `{answer: string, sources: [{title, link, published}], audit_id: string | null, outcome: string}`. See [ResearchAgent](../07-agents/agents/research-agent.md) for the orchestration behind it; the router itself (`backend/app/api/v1/agents.py`) contains no business logic, per the convention below.

## `POST /api/v1/missions` (implemented, Gate 3)

Requires authentication — the mission's owner is always the authenticated user, resolved server-side, never from the request body. Request: `{goal: string}` — no other field exists, so a client cannot supply `user_id`, `xp_awarded`, `permission`, `risk`, or `agent_name` as authoritative values even if it tries (see [Mission System](../08-modules/mission-system.md)). Response: `{id, status, answer, sources: [{title, link, published}], xp_awarded, failure_reason}`. Orchestration is `MissionService` (`backend/app/services/mission_service.py`), which wraps `ResearchAgent.research()` with no AI/tool/permission logic of its own; the router (`backend/app/api/v1/missions.py`) is thin. `GET /api/v1/missions` (list) is deferred — not needed for the MVP feedback loop.

## `/api/v1/conversations` (implemented, Gate 4)

All routes require authentication; every `conversation_id` in a URL is re-validated against the authenticated user server-side (`ConversationRepository.get_for_user`) before any read or write — a client can never reach another user's conversation, and gets the same 404 whether the id doesn't exist or belongs to someone else, never a 403 that would confirm existence.

- `POST /conversations` → `{id, created_at, updated_at}`.
- `GET /conversations` → list, most recently updated first.
- `POST /conversations/{id}/messages` — request `{content: string}` (no other field exists, so no `user_id`/`role` can be supplied by a client with any effect). Response: `{user_message: {...}, assistant_message: {...}}`, each `{id, role, content, created_at}`.
- `GET /conversations/{id}/messages` — full history, oldest first.
- `DELETE /conversations/{id}` — hard delete (204), cascades to its messages at the database level (`ON DELETE CASCADE`).

Orchestration is `ConversationService` (`backend/app/services/conversation_service.py`): reads a bounded window of the conversation's own prior messages (see [Context management](../06-ai/context-management.md) for how the window size was chosen), calls `AIService.generate()` with that history, and persists both turns. No AI/tool/permission logic of its own. See [Memory](../06-ai/memory.md) for what is and isn't in scope (session-only, no durable cross-conversation memory).

## `/api/v1/news` (implemented, Gate 5)

Both routes require authentication — reusing the existing `get_current_user` dependency, no dedicated News permission scope (nothing in the documentation calls for one, and the digest isn't per-user). This is a deliberate consistency choice (same auth boundary as every other endpoint since Gate 2), not a personalization requirement — see [News Intelligence](../08-modules/news-intelligence.md).

- `POST /news/refresh` — declares no request body; triggers `NewsService.refresh()` across every server-seeded `Source`. Response: `{results: [{source_key, items_found, items_new, error}], items_new_total}`. A failing source doesn't block the others.
- `GET /news` — the current digest, most recently published first. Response items: `{id, title, link, excerpt, source_name, published_at}` — `title`/`excerpt` are always the source's own RSS text, verbatim; **no AI summarization exists in this pipeline** (see [ADR-0014](../adr/0014-defer-ai-summarization.md)).

`Source` rows are never client-writable — seeded exclusively by a migration (`backend/migrations/versions/909bb72ee271_...py`), same "code change + review" posture as `read_rss_feed`'s `RSS_ALLOWLIST`. `NewsItem.link` is unique — idempotent-by-URL persistence, not the deferred semantic-deduplication pipeline stage.

## Deprecation: `/ai/chat`

Superseded by `POST /api/v1/conversations/{id}/messages`, which is authenticated and persists history — `/ai/chat` is neither. As of Gate 4, no frontend code calls it (`AiChatScreen` was migrated to `/conversations`). Rather than break the Phase 0 contract outright, the route is marked `deprecated=True` (surfaced in the OpenAPI docs) and kept fully functional; it has no scheduled removal date.

## Conventions

- Versioned from day one (`/api/v1/...`) — followed.
- Consistent error envelope (see [error-handling.md](error-handling.md)) — followed.
- Every mutating/permissioned endpoint enforces the same permission model used by agents (see [07-agents/permissions.md](../07-agents/permissions.md)) — followed for `/agents/research`; humans and agents go through the same `authorize_tool_call` path.
- Routers stay thin; orchestration lives in services/agents, not route handlers — followed (`app/api/v1/agents.py` is ~15 lines, `app/api/v1/missions.py` is ~15 lines).
- Client-supplied request bodies never carry authority fields (user identity, XP, permission, risk) — enforced structurally by the request schema, not by convention alone (see `MissionRequest`).

## Related documentation

- [Architecture](architecture.md)
- [Authentication](authentication.md)
- [Authorization](authorization.md)
- [ResearchAgent](../07-agents/agents/research-agent.md)
- [Mission System](../08-modules/mission-system.md)
- [Memory](../06-ai/memory.md)
- [Context management](../06-ai/context-management.md)
- [News Intelligence](../08-modules/news-intelligence.md)
- [ADR-0014: Defer AI summarization](../adr/0014-defer-ai-summarization.md)
