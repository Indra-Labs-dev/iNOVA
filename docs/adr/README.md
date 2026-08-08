# Architecture Decision Records

**Status:** Living index
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Index every ADR for iNOVA. See [02-architecture/architecture-decisions.md](../02-architecture/architecture-decisions.md) for why ADRs are used here.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-flutter-frontend.md) | Flutter as primary frontend | Accepted |
| [0002](0002-threejs-3d-world.md) | Three.js/WebGL for the 3D world | Accepted |
| [0003](0003-rive-mascot.md) | Rive for the mascot | Accepted |
| [0004](0004-fastapi-backend.md) | FastAPI as backend framework | Accepted |
| [0005](0005-ollama-local-llm.md) | Ollama / local LLM for current development | Accepted |
| [0006](0006-llmprovider-abstraction.md) | LLMProvider abstraction | Accepted |
| [0007](0007-agent-permissions.md) | Explicit agent permission model | Accepted |
| [0008](0008-modular-architecture.md) | Modular architecture over monolithic files/modules | Accepted |
| [0009](0009-mascot-naming-aira.md) | Mascot naming — Aira | Accepted |
| [0010](0010-authentication-approach.md) | Authentication — in-house JWT + revocable sessions | Accepted |
| [0011](0011-alembic-migrations.md) | Database migrations — Alembic | Accepted |

## Adding a new ADR

Copy [ADR-XXXX-template.md](ADR-XXXX-template.md), number it sequentially, fill in Status/Context/Decision/Consequences/Alternatives considered, and add a row above.

## Related documentation

- [Architecture decisions (process)](../02-architecture/architecture-decisions.md)
