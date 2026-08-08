# iNOVA — Project Status

**Last Updated:** 2026-08-08
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
| Documentation (`docs/`) | IN PROGRESS | This documentation set itself — first full pass completed 2026-08-08; needs review as implementation begins. |
| Frontend (Flutter shell) | NOT STARTED | No `pubspec.yaml`, no `lib/` directory. |
| 3D World (Three.js) | NOT STARTED | No 3D code. |
| Mascot (Aira/Rive) | NOT STARTED | Only a concept image (`mascotte-aira.png`) exists at repo root; no Rive file, no character bible. Name officially confirmed as Aira, see [ADR-0009](adr/0009-mascot-naming-aira.md). |
| Backend (FastAPI) | NOT STARTED | No backend directory, no `requirements.txt`/`pyproject.toml`. |
| AI Core / LLMProvider | NOT STARTED | Ollama is usable locally today (external tool), but no `LLMProvider` code exists. |
| Agents (all 9) | NOT STARTED | No agent runtime, no agent code. |
| Cybersecurity Hub | NOT STARTED | |
| Programming Hub | NOT STARTED | |
| News Intelligence | NOT STARTED | |
| Research Hub | NOT STARTED | |
| OSINT Hub | NOT STARTED | |
| Learning Hub | NOT STARTED | |
| Productivity Hub | NOT STARTED | |
| Device Hub | NOT STARTED | |
| Cloud Hub | NOT STARTED | |
| Mission System | NOT STARTED | |
| Gamification | NOT STARTED | |
| Database (PostgreSQL schema) | NOT STARTED | No migrations, no ORM models. |
| Testing | NOT STARTED | No test framework configured, no tests. |
| DevOps (Docker/CI/CD) | NOT STARTED | No `Dockerfile`, no `docker-compose.yml`, no GitHub Actions workflow. |
| Git repository | STABLE | Initialized, connected to `git@github.com:Indra-Labs-dev/iNOVA.git`, `main` branch, 1 commit so far containing a placeholder `README.md`. |

## What exists in the repository today

- `iNOVA_MASTER_CONTEXT.md` — original product vision document.
- `iNOVA_CAHIER_DES_CHARGES.md` — derived specifications: MVP scope, architecture, external dependencies, budget, risks (includes the local-LLM/4GB-VRAM decision).
- `iNOVA_OBJECTIFS_FONCTIONNALITES_STACK.md` — detailed objective/feature/stack reference for the full product.
- `docs/` — this documentation set.
- `logo.png`, `mascotte-aira.png` — brand/concept assets.
- `README.md` — currently an 8-byte placeholder (`# iNOVA`).

## Decisions already locked in (documented, not yet implemented)

- Frontend: Flutter ([ADR-0001](adr/0001-flutter-frontend.md)).
- 3D: Three.js/WebGL ([ADR-0002](adr/0002-threejs-3d-world.md)).
- Mascot animation: Rive ([ADR-0003](adr/0003-rive-mascot.md)).
- Backend: FastAPI ([ADR-0004](adr/0004-fastapi-backend.md)).
- AI: Ollama local, `qwen2.5:3b-instruct-q4_K_M`, on ~4GB VRAM hardware ([ADR-0005](adr/0005-ollama-local-llm.md)).
- AI abstraction: `LLMProvider` interface required from the start ([ADR-0006](adr/0006-llmprovider-abstraction.md)).
- Agent permission model: mandatory scoped permissions/risk levels ([ADR-0007](adr/0007-agent-permissions.md)).
- Modular architecture, no monoliths ([ADR-0008](adr/0008-modular-architecture.md)).
- Mascot naming: product is **iNOVA**, mascot/companion is **Aira** — not interchangeable ([ADR-0009](adr/0009-mascot-naming-aira.md)).

See also [docs/ARCHITECTURE_FREEZE.md](ARCHITECTURE_FREEZE.md) for the full architecture freeze produced after the 2026-08-08 documentation review.

## Recommended next step

Start Phase 0 ([16-roadmap/phases.md](16-roadmap/phases.md)): repository scaffolding for `frontend/` (Flutter) and `backend/` (FastAPI), a minimal auth flow, and the first PostgreSQL migration — see [15-development/setup.md](15-development/setup.md) for what's still `TODO` to make that possible.

## Related documentation

- [Scope](00-overview/scope.md)
- [Roadmap](16-roadmap/roadmap.md)
- [MVP](16-roadmap/mvp.md)
