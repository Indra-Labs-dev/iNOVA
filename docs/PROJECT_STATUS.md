# iNOVA — Project Status

**Last Updated:** 2026-08-08 (Gate 6 — 3D World Feasibility Spike)
**Owner:** Archange Elie Yatte

## Purpose

The single authoritative source for what actually exists in this repository right now. Unlike every other document in `docs/`, which describes target architecture and product scope, this file reflects reality only. If this file and any other document disagree, this file is correct — update the other document, not this one.

## Status legend

```text
NOT STARTED   — nothing built, not even scaffolding
PLANNED       — documented target, no code
IN PROGRESS   — actively being built, incomplete
PARTIAL       — some functionality works, meaningfully incomplete
IMPLEMENTED   — functionally complete, not yet tested
TESTED        — implemented and covered by tests
STABLE        — tested and running reliably over time
DEPRECATED    — was built, now retired
```

## Status table

| Module | Status | Notes |
|---|---|---|
| Documentation (`docs/`) | IN PROGRESS | 165+ files; reviewed and audited 2026-08-08 — see [ARCHITECTURE_FREEZE.md](ARCHITECTURE_FREEZE.md). |
| Frontend (Flutter shell) | TESTED | Riverpod, minimal routing (4 routes), dark theme, `AiChatScreen` (Gate 4: real multi-turn chat, server-persisted history) + `ResearchScreen` (Gate 2) + `MissionScreen` (Gate 3, "Mission complete +X XP" or real failure reason) + `NewsScreen` (Gate 5: extractive digest, no AI summary rendered). 21/21 tests pass, `flutter analyze` clean, manually verified in a real browser against the real backend for all four screens, including a real reload + re-login round trip for chat history and a real digest refresh against the live public RSS feeds. |
| 3D World (Three.js) | NOT STARTED | Phase 3. Gate 6 (2026-08-08) ran an isolated, deletable feasibility spike, not the real 3D World: measured that Flutter Web can host and drive Three.js/WebGL with reliable bidirectional communication via native `dart:js_interop` + vendored (MIT, npm-sourced) Three.js, no CDN for the 3D engine, verified against a real `--release` build — verdict READY for that question. Also found, separately, that Flutter's default release build fetches CanvasKit/fonts from `gstatic.com`, which must be fixed (shared `web/flutter_bootstrap.js` override) before real 3D work begins. See [Gate 6 report](16-roadmap/gate-6-3d-spike-report.md). Spike code lives at `frontend/lib/spike_3d/`, `frontend/web/spike3d/` — fully separate from this row's "not started" real implementation. |
| Mascot (Aira/Rive) | NOT STARTED | Name confirmed ([ADR-0009](adr/0009-mascot-naming-aira.md)); static placeholder only (`AiraPlaceholder`, real concept art) — no Rive integration, that's Phase 2. Blocked on a real `.riv` asset (Rive's editor is an external design tool, not something a coding Gate can author) — see the Gate 5 proposal's alternatives comparison for why News Intelligence was prioritized instead. |
| Backend (FastAPI) | TESTED | `GET /health`, `POST/GET /auth/*`, `POST /ai/chat` (deprecated, kept working), `POST /agents/research`, `POST /missions`, `POST/GET /conversations`, `POST/GET .../messages`, `DELETE /conversations/{id}`, `POST /news/refresh`, `GET /news`. 148/148 default tests pass (SQLite + fakes) + 6/6 real-Ollama-marked tests. Verified end-to-end against real PostgreSQL and real Ollama, including through the actual Flutter UI, for `/agents/research`, `/missions`, `/conversations`, and (Postgres + real public RSS feeds, no Ollama involved) `/news`. |
| AI Core / LLMProvider | TESTED | `LLMProvider.generate(message, tools?, system?, history?) -> LLMResponse`, implemented in `OllamaProvider`. Tool-calling measured (Gate 1, [ADR-0012](adr/0012-tool-calling-contract.md)) and consumed for real by `ResearchAgent` (Gate 2). Bounded conversation history (`history` param, Gate 4) consumed by `ConversationService` — see [context-management.md](06-ai/context-management.md). Still no Agent Router, no durable cross-conversation memory. |
| Authentication | TESTED | In-house JWT + revocable refresh sessions ([ADR-0010](adr/0010-authentication-approach.md)). Now also gates `/agents/research`. Email verification and MFA remain `[PLANNED]`. |
| Tool Registry | TESTED | Static, in-code (`ToolRegistry`, [ADR-0013](adr/0013-static-tool-registry.md)). One real tool registered: `read_rss_feed`. No API surface can register/modify a tool — by construction, not policy. |
| ResearchAgent | TESTED | Implemented ([docs/07-agents/agents/research-agent.md](07-agents/agents/research-agent.md)): permission check, argument validation, tool execution, audit logging, AI synthesis, source attribution. Verified live end to end (real Ollama, real RSS feed, real PostgreSQL audit entry) through the actual Flutter app. Security-tested: hallucinated tool, invalid arguments, permission-denied, and a synthetic MEDIUM/HIGH tool's confirmation gate all proven to block execution. |
| AuditLog | TESTED | `audit_logs` table, one migration, `AuditLogRepository`. Records success, permission-denial, invalid-tool-call, invalid-arguments, confirmation-required, and execution-failure outcomes — verified in tests and against a real database. |
| Conversation Memory (AI Companion) | PARTIAL | Session-only (Gate 4): `ConversationService` + bounded-history window (default 20, chosen from a real measured experiment — see [memory.md](06-ai/memory.md), [context-management.md](06-ai/context-management.md)). Strict per-user isolation tested (unit + live, cross-user read/write/delete all rejected). Durable cross-conversation memory remains explicitly `[PLANNED]`, out of scope by design. |
| Agents (other 8) | NOT STARTED | Phase 4+. |
| Cybersecurity Hub | NOT STARTED | Phase 6. |
| Programming Hub | NOT STARTED | Phase 6. |
| News Intelligence | PARTIAL | Gate 5 — RSS ingestion, normalization, persistence, and source attribution IMPLEMENTED/TESTED. AI summarization DEFERRED — measured against the real model and found unreliable (0/9 on the required fact/inference distinction, plus one confirmed factual inversion), see [ADR-0014](adr/0014-defer-ai-summarization.md). Classification, semantic deduplication, cross-checking, personalization remain PLANNED (Phase 5). See [news-intelligence.md](08-modules/news-intelligence.md). |
| Research Hub | PARTIAL | `ResearchAgent`'s `read_rss_feed` slice only — the full hub (dedup, classification, multiple source types) is Phase 5. |
| OSINT Hub | NOT STARTED | Future. |
| Learning Hub | NOT STARTED | Phase 7. |
| Productivity Hub | NOT STARTED | Phase 7. |
| Device Hub | NOT STARTED | Phase 7. |
| Cloud Hub | NOT STARTED | Phase 7. |
| Mission System | PARTIAL | MVP slice implemented (Gate 3): `MissionService` orchestrates one `ResearchAgent` call per mission, no Agent Router/multi-agent/task queue. Full multi-agent version remains Phase 4+. See [mission-system.md](08-modules/mission-system.md). |
| Gamification | PARTIAL | XP only (Gate 3): additive-only `UserProgress`, awarded server-side on mission success. No levels, streaks, achievements, or gamification UI yet. See [gamification.md](08-modules/gamification.md). |
| Database (PostgreSQL schema) | TESTED | `users`, `sessions`, `audit_logs`, `missions`, `user_progress`, `conversations`, `messages`, `sources`, `news_items` — reviewed, autogenerated Alembic migrations. Upgrade/downgrade verified against real PostgreSQL 16, including real `ON DELETE CASCADE` behavior for `messages` (SQLite's test engine doesn't enforce this, so it's verified against real Postgres data, not just schema) and real seed-data re-insertion for `sources` across the cycle. Other entities added only as their owning feature needs them. |
| Testing | IMPLEMENTED | pytest (backend, 148 default + 6 real-Ollama) + `flutter test` (frontend, 21) both wired and passing. No CI yet. |
| DevOps (Docker/CI/CD) | PARTIAL | `docker-compose.yml` with PostgreSQL only (deliberately minimal). No CI/CD pipeline, no staging/production deployment. |
| Git repository | STABLE | `Indra-Labs-dev/iNOVA`, `main` branch. History untouched by this work. |

## What exists in the repository today

- `iNOVA_MASTER_CONTEXT.md`, `iNOVA_CAHIER_DES_CHARGES.md`, `iNOVA_OBJECTIFS_FONCTIONNALITES_STACK.md` — product vision and specifications.
- `docs/` — full technical/product documentation set + [ARCHITECTURE_FREEZE.md](ARCHITECTURE_FREEZE.md).
- `backend/` — FastAPI application, including `app/agents/`, `app/tools/` (Gate 2), `app/services/mission_service.py`, `app/models/mission.py`, `app/models/user_progress.py` (Gate 3), `app/services/conversation_service.py`, `app/models/conversation.py`, `app/models/message.py` (Gate 4), `app/services/news_service.py`, `app/models/source.py`, `app/models/news_item.py` (new in Gate 5).
- `frontend/` — Flutter application, including `features/research/` and `core/auth/` (Gate 2), `features/missions/` (Gate 3), a rebuilt `features/ai_chat/` (Gate 4), `features/news/` (new in Gate 5).
- `docker-compose.yml` — PostgreSQL for local development.
- `logo.png`, `mascotte-aira.png` — brand/concept assets (also bundled in `frontend/assets/images/`).
- `README.md` — project entry point with author/project/AI companion attribution.

## Decisions locked in

- Frontend: Flutter ([ADR-0001](adr/0001-flutter-frontend.md)) — **implemented**.
- 3D: Three.js/WebGL ([ADR-0002](adr/0002-threejs-3d-world.md)) — not yet implemented.
- Mascot animation: Rive ([ADR-0003](adr/0003-rive-mascot.md)) — not yet implemented (placeholder only).
- Backend: FastAPI ([ADR-0004](adr/0004-fastapi-backend.md)) — **implemented**.
- AI: Ollama local ([ADR-0005](adr/0005-ollama-local-llm.md), incl. 2026-08-08 addendum on the `qwen2.5-coder:3b` tag substitution) — **implemented**.
- AI abstraction: `LLMProvider` interface ([ADR-0006](adr/0006-llmprovider-abstraction.md)) — **implemented**.
- Agent permission model ([ADR-0007](adr/0007-agent-permissions.md)) — **implemented and exercised** by ResearchAgent.
- Modular architecture ([ADR-0008](adr/0008-modular-architecture.md)) — followed throughout.
- Mascot naming: **iNOVA** (product) / **Aira** (mascot) ([ADR-0009](adr/0009-mascot-naming-aira.md)) — reflected in code and docs.
- Authentication: in-house JWT + revocable sessions ([ADR-0010](adr/0010-authentication-approach.md)) — **implemented**.
- DB migrations: Alembic ([ADR-0011](adr/0011-alembic-migrations.md)) — **implemented**.
- Tool-calling contract + strategy (native, strictly validated) ([ADR-0012](adr/0012-tool-calling-contract.md)) — **implemented and measured**.
- Static in-code Tool Registry ([ADR-0013](adr/0013-static-tool-registry.md)) — **implemented**.
- AI summarization deferred for News Intelligence ([ADR-0014](adr/0014-defer-ai-summarization.md)) — **measured and deferred**, not implemented; revisit only via a fresh, independent experiment.

## Known gaps / deliberately deferred

- No CI/CD pipeline yet.
- No email verification, no MFA, no per-user permission grant table (every authenticated user implicitly has `research.read` — see [research-agent.md](07-agents/agents/research-agent.md) "Permissions").
- No dedicated frontend auth feature — `ResearchScreen` has a minimal inline, unpersisted sign-in gate (see `frontend/lib/features/research/presentation/research_screen.dart`), not a real session/login feature.
- Redis not introduced (no documented use case needs it yet).
- Rate limiting on auth/AI/agents endpoints not implemented.
- `Nova*` design-system component-prefix naming vs. `Aira*` remains an open decision.
- Multi-tool discrimination (does the model choose correctly among *several* real tools) is untested — Gate 1/2 only ever offered one tool at a time. Re-test before Phase 4's Agent Router.
- `GET /api/v1/missions` (mission history/list) is deferred — the MVP only needs the immediate "Mission complete +X XP" feedback from `POST /missions`.
- Real-Ollama-marked tests occasionally show the model responding with plain text instead of a tool call (observed during Gate 3 and Gate 4 live verification) — consistent with Gate 1's finding that tool-call reliability is high but not literally 100%; the relevant failure paths (mission marked `failed`, real reason preserved; a chat reply that's just wrong rather than a masked error) handle this correctly, nothing is silently hidden.
- Durable, cross-conversation memory (`Memory` entity, [06-ai/memory.md](06-ai/memory.md) "Target scope (post-MVP)") remains deliberately out of scope — Gate 4 only implemented session-scoped history within a single conversation.
- The Flutter access token still isn't persisted across a page reload (`core/auth/auth_session.dart`) — a real reload requires signing in again; conversation history itself does survive, because it's stored server-side, not in client memory. Same documented Phase 0 limitation as the Research/Missions sign-in gates.
- `POST /api/v1/ai/chat` is now deprecated (`deprecated=True`, unused by the frontend since Gate 4) but kept working rather than removed — see [09-backend/api-design.md](09-backend/api-design.md).
- AI summarization for News Intelligence is deliberately deferred, not implemented — see [ADR-0014](adr/0014-defer-ai-summarization.md). The digest shows the source's own RSS text (title/excerpt), never AI-generated text. No scheduler/Celery/Redis/RQ was introduced for News ingestion — refresh stays synchronous, triggered only by `POST /news/refresh`, per the explicit Gate 5 GO.
- News Intelligence's `Source` catalog is exactly the 2 feeds already allowlisted for `read_rss_feed` (`python_blog`, `github_blog`) — expanding it requires a code change + review (migration), same posture as the tool allowlist, never a runtime/API action.
- Flutter's default web release build fetches CanvasKit and a Roboto font from `gstatic.com` (Flutter platform default, unrelated to Three.js) — discovered during the Gate 6 spike's production-build verification, not yet fixed because the fix (`web/flutter_bootstrap.js`) is a shared, whole-app file out of that spike's isolated scope. See [Gate 6 report](16-roadmap/gate-6-3d-spike-report.md) §5.
- Gate 6's 3D spike (`frontend/lib/spike_3d/`, `frontend/web/spike3d/`) is a deletable feasibility exercise, not the real 3D World — no ADR was written for 3D architecture yet, per explicit instruction to wait until after measurement and before real 3D World implementation.

## Recommended next step

Gate 6 is complete: an isolated feasibility spike measured that Flutter Web can host and drive
Three.js/WebGL with reliable bidirectional communication, fully locally (vendored Three.js, no
CDN for the engine), verified against both dev mode and a real `--release` build — verdict
READY for that question. A separate, real finding (Flutter's own CanvasKit/font CDN default in
release builds) was measured, documented, and deliberately left unresolved inside the spike
because fixing it touches a file shared with the already-shipped app. See the
[Gate 6 report](16-roadmap/gate-6-3d-spike-report.md) for full measurements and the Gate 7
proposal (first real 3D World increment). Per the gated plan, do not start Gate 7 or any other
next vertical (durable cross-conversation memory, Agent Router, Cybersecurity Hub, richer
gamification, Aira's visual/Rive layer, revisiting AI summarization) without an explicit
go-ahead.

## Related documentation

- [Architecture Freeze](ARCHITECTURE_FREEZE.md)
- [Scope](00-overview/scope.md)
- [Roadmap](16-roadmap/roadmap.md)
- [MVP](16-roadmap/mvp.md)
- [ResearchAgent](07-agents/agents/research-agent.md)
- [Mission System](08-modules/mission-system.md)
- [Gamification](08-modules/gamification.md)
- [Memory](06-ai/memory.md)
- [Context management](06-ai/context-management.md)
- [News Intelligence](08-modules/news-intelligence.md)
- [ADR-0014: Defer AI summarization](adr/0014-defer-ai-summarization.md)
- [Gate 6: 3D World feasibility spike report](16-roadmap/gate-6-3d-spike-report.md)
