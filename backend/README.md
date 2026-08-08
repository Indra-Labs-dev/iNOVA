# iNOVA Backend

Copyright (c) 2026 Archange Elie Yatte (AEY)

FastAPI backend for iNOVA — Phase 0 Foundation scope only. See [../docs/ARCHITECTURE_FREEZE.md](../docs/ARCHITECTURE_FREEZE.md) and [../docs/09-backend/architecture.md](../docs/09-backend/architecture.md) for the full architecture this scaffold implements a slice of.

## What's here (Phase 0)

- `GET /api/v1/health`
- `POST /api/v1/auth/{register,login,refresh,logout}`, `GET /api/v1/auth/me`
- `POST /api/v1/ai/chat` — talks to a local Ollama instance through the `LLMProvider` abstraction
- PostgreSQL via SQLAlchemy + Alembic (`users`, `sessions` tables only)

Everything else in `docs/09-backend/api-design.md`'s endpoint list (`/agents`, `/tools`, `/missions`, ...) is `[PLANNED]`, not here — see [../docs/16-roadmap/mvp.md](../docs/16-roadmap/mvp.md) for what's deliberately deferred.

## Setup

Requires: Python 3.11+, [uv](https://github.com/astral-sh/uv) (or pip), Docker, a local Ollama with a model pulled (see `.env.example` for the configured tag).

```bash
# from backend/
uv venv .venv
uv pip install -e ".[dev]" --python .venv/bin/python
cp .env.example .env   # edit JWT_SECRET_KEY at minimum

# start Postgres (from repo root)
cd .. && docker compose up -d postgres && cd backend

# apply migrations
.venv/bin/alembic upgrade head

# run the dev server
.venv/bin/uvicorn app.main:app --reload --port 8010
```

## Tests

```bash
.venv/bin/python -m pytest -v
```

No test depends on a running Postgres or Ollama — SQLite in-memory and a fake `LLMProvider` are used (see `tests/conftest.py`). Run against the real stack manually via the setup steps above to validate the actual integration.

## Project structure

```text
app/
├── main.py            FastAPI app factory, CORS, error handlers, router mounting
├── core/               config, database session, security (JWT/hashing), error envelope
├── api/v1/             route handlers (health, auth, ai)
├── models/              SQLAlchemy ORM models
├── schemas/             Pydantic request/response models
├── repositories/        DB access, no business logic
├── services/             business logic, no DB/HTTP details
└── ai/                  LLMProvider interface + OllamaProvider + AIService
```

See [../docs/02-architecture/components.md](../docs/02-architecture/components.md) for the target shape this will grow into.
