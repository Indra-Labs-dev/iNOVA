# iNOVA — Architecture Freeze

**Date:** 2026-08-08
**Owner:** Archange Elie Yatte
**Status:** READY — architecture frozen for Phase 0 start, pending open decisions listed below (none of which block Phase 0 scaffolding)

## Purpose

Close out the documentation review that produced `docs/` (163 files, 2026-08-08) and the subsequent naming/consistency audit. This is the checkpoint before any code is written. It does not introduce new decisions — it consolidates and confirms decisions already recorded across `docs/`, and lists what remains genuinely open.

## How to read this document

This freeze does not replace any individual document — it is an index confirming their state agrees with each other. Where this document and a specific technical document (e.g. an ADR) disagree in the future, the specific document wins and this freeze should be regenerated.

---

## 1. Confirmed decisions

| Decision | Record |
|---|---|
| Frontend: Flutter (Dart) + Riverpod | [ADR-0001](adr/0001-flutter-frontend.md) |
| 3D world: Three.js/WebGL, GLTF/GLB assets | [ADR-0002](adr/0002-threejs-3d-world.md) |
| Mascot animation: Rive (+ Lottie for one-off effects) | [ADR-0003](adr/0003-rive-mascot.md) |
| Backend: Python + FastAPI | [ADR-0004](adr/0004-fastapi-backend.md) |
| AI runtime: Ollama, local, `qwen2.5:3b-instruct-q4_K_M` on ~4GB VRAM (revisable) | [ADR-0005](adr/0005-ollama-local-llm.md) |
| AI abstraction: mandatory `LLMProvider` interface, no direct provider calls in agents/AI Core | [ADR-0006](adr/0006-llmprovider-abstraction.md) |
| Agent permission model: scoped permission + risk level + confirmation gate per tool, server-side validated | [ADR-0007](adr/0007-agent-permissions.md) |
| Modular architecture: small cohesive modules, no monoliths, cross-module comms via core/event bus only | [ADR-0008](adr/0008-modular-architecture.md) |
| Mascot naming: product is **iNOVA**, mascot/companion is **Aira** — never interchangeable | [ADR-0009](adr/0009-mascot-naming-aira.md) |
| Database: PostgreSQL (structured domain data), Redis (cache + event bus, never source of truth) | [10-data/data-architecture.md](10-data/data-architecture.md) |
| Scraping/ingestion policy: official API > RSS > permitted public source; never bypass anti-bot/access control | [11-intelligence/scraping-policy.md](11-intelligence/scraping-policy.md) |
| MVP is a vertical slice (AI + Agent + Data + Aira + 2D/3D), not sequential phase completion | [16-roadmap/mvp.md](16-roadmap/mvp.md), [16-roadmap/phases.md](16-roadmap/phases.md) |

## 2. Open decisions

None of these block Phase 0 scaffolding start, but each is flagged with its trigger point. No arbitrary choice has been made for any of them — see the linked document for full options and decision criteria.

| Decision | Options summarized | Must be resolved before |
|---|---|---|
| Authentication: in-house vs. managed (Auth0/Clerk/Firebase) | See [09-backend/authentication.md](09-backend/authentication.md) | `User`/`Session` entities are implemented (Phase 0) |
| DB migration tool: Alembic vs. raw SQL | See [10-data/migrations.md](10-data/migrations.md) | First migration is written (Phase 0) |
| Async job mechanism: in-process asyncio vs. Celery vs. RQ | See [09-backend/background-jobs.md](09-backend/background-jobs.md) | First async workload needing persistence/retry exists (likely Phase 5) |
| Knowledge Graph storage: relational edge-table vs. PostgreSQL graph extension vs. dedicated graph DB | See [10-data/knowledge-graph.md](10-data/knowledge-graph.md) | Knowledge Graph module work begins (Future phase, not blocking) |
| Git branch naming convention | See [15-development/branching.md](15-development/branching.md) | A second contributor joins, or before it matters for history clarity |
| API error envelope format | See [09-backend/error-handling.md](09-backend/error-handling.md) | First API endpoint ships (Phase 0/1) |
| `Nova*` design-system component prefix vs. renaming to match Aira | See [03-frontend/design-system.md](03-frontend/design-system.md) naming note | First shared UI component is implemented (Phase 0/1) |

## 3. Current constraints

- **Hardware**: local LLM development is bounded by ~4GB VRAM. This shapes model choice ([06-ai/model-strategy.md](06-ai/model-strategy.md)) and, downstream, agent tool-call reliability expectations ([12-security/agent-security.md](12-security/agent-security.md)). Documented as revisable, not permanent.
- **Team**: single author (Archange Elie Yatte) at this stage — process documents ([15-development/](15-development/git-workflow.md)) are intentionally lightweight until a second contributor joins.
- **No code exists yet**: every module in [PROJECT_STATUS.md](PROJECT_STATUS.md) is `NOT STARTED` except the documentation itself. This freeze authorizes starting Phase 0 scaffolding, not claiming any implementation progress.
- **Budget**: MVP hosting target is a single VPS + domain (~20-40€/month), no recurring LLM API cost by design — see [iNOVA_CAHIER_DES_CHARGES.md §5.6](../iNOVA_CAHIER_DES_CHARGES.md).

## 4. Architectural boundaries

```text
Flutter        → Presentation / application UI (shell, navigation, dashboards, forms)
Riverpod       → Frontend state / dependency management
Three.js       → 3D visualization / world (embedded in, not owned by, Flutter)
Rive           → Aira animation / state machine
FastAPI        → Backend API (auth, routing, validation, orchestration entrypoint)
AI Core        → AI orchestration / context / providers (never trusts model output blindly)
Agents         → Specialized autonomous workflows, permissioned per tool
Tools          → Controlled capabilities, schema-validated, risk-classified
Permissions    → Authorization boundary — same enforcement path for humans and agents
PostgreSQL     → Persistent relational data (single source of truth)
Redis          → Cache / events / transient state — never the only copy of durable data
Ollama         → Local LLM runtime, accessed only through LLMProvider
```

Full detail: [02-architecture/overview.md](02-architecture/overview.md), [02-architecture/components.md](02-architecture/components.md).

Each layer's responsibility is exclusive: no layer duplicates another's concern (e.g. Flutter never renders 3D directly; Three.js never owns application/business state; Agents never bypass the Tools/Permissions boundary; Redis never holds data that must survive a flush).

## 5. Forbidden shortcuts

These are explicit, not implied — violating any of them is a defect, not a style preference:

- Executing AI/agent-produced output (tool calls, commands, code) without server-side schema and permission validation.
- Any HIGH-risk tool executing without a mandatory user confirmation gate.
- Any agent tool call, successful or not, skipping its audit log entry.
- Direct provider-specific LLM client usage in AI Core or agent code, bypassing `LLMProvider`.
- Secrets committed to source control, hard-coded, or logged at INFO level or above.
- Building the full version of a later-phase module (full Cybersecurity Hub, full Agent Hub, full Programming Hub, OSINT, Learning, Productivity, Cloud) to satisfy an MVP requirement — build only the documented MVP slice ([16-roadmap/mvp.md](16-roadmap/mvp.md)).
- Scraping mechanisms that bypass robots.txt, ToS, or anti-bot protections.
- Presenting a `[PLANNED]` feature as `[IMPLEMENTED]` anywhere in documentation or code comments.
- Monolithic files/modules, or cross-feature Dart/Python imports bypassing `core/`/the event bus.
- Renaming or reintroducing "Nova" as the mascot name, or using "Aira" as an alternate product name.

## 6. Next implementation phase

**Phase 0 — Foundation** (see [16-roadmap/phases.md](16-roadmap/phases.md)):

1. Resolve the two Phase-0-blocking open decisions first: authentication approach and DB migration tool (§2 above) — both shape the first schema.
2. Scaffold `backend/` (FastAPI) and `frontend/` (Flutter) per [02-architecture/components.md](02-architecture/components.md) and [03-frontend/architecture.md](03-frontend/architecture.md) directory conventions.
3. Implement minimal auth (per whichever option is chosen) and the first PostgreSQL migration for the `User`/`Session` entities.
4. Stand up the local dev loop end to end: backend running, frontend running, Ollama reachable — see [15-development/setup.md](15-development/setup.md) for what's currently `TODO` to make this possible.
5. Do not start Flutter screens beyond a bare shell, 3D scene work, Rive integration, or any agent code until step 4 is working — per [00-overview/product-philosophy.md](00-overview/product-philosophy.md), architecture and security precede functionality.

## Related documentation

- [PROJECT_STATUS.md](PROJECT_STATUS.md)
- [16-roadmap/phases.md](16-roadmap/phases.md)
- [16-roadmap/mvp.md](16-roadmap/mvp.md)
- [adr/README.md](adr/README.md)
