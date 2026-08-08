# Setup

**Status:** [PARTIAL] — only documentation and Ollama setup are currently actionable; frontend/backend do not exist yet
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Let a new contributor (human or AI) get iNOVA running locally, step by step, with clear markers for what isn't buildable yet.

## Scope

Local development setup only. Environment tiers are in [13-devops/environments.md](../13-devops/environments.md).

## 1. Prerequisites

- Git, GitHub access to `Indra-Labs-dev/iNOVA`.
- Flutter SDK — `TODO — PLANNED`, version to be pinned once the frontend scaffold is created.
- Python (version `TODO — PLANNED`, to be pinned with the backend scaffold), PostgreSQL, Redis.
- Ollama (see step 7) — this is the one runtime dependency usable **today**.

## 2. Install dependencies

`TODO — PLANNED`. No `pubspec.yaml` or `requirements.txt`/`pyproject.toml` exists yet. This section will list exact install commands once [03-frontend/architecture.md](../03-frontend/architecture.md) and [09-backend/architecture.md](../09-backend/architecture.md) scaffolds exist.

## 3. Configure environment variables

`TODO — PLANNED`. No `.env.example` exists yet. Per [12-security/secrets.md](../12-security/secrets.md), this file must never contain real secrets — only variable names and dummy/example values.

## 4. Launch supporting services

`TODO — PLANNED` — target: `docker-compose up` for PostgreSQL and Redis (see [13-devops/docker.md](../13-devops/docker.md)).

## 5. Launch the frontend

`TODO — PLANNED` — target: `flutter run -d chrome` (web target) once the Flutter shell exists.

## 6. Launch the backend

`TODO — PLANNED` — target: `uvicorn` dev server once the FastAPI scaffold exists (see [09-backend/fastapi.md](../09-backend/fastapi.md)).

## 7. Launch Ollama (actionable today)

```bash
ollama pull qwen2.5:3b-instruct-q4_K_M
ollama run qwen2.5:3b-instruct-q4_K_M
```

See [06-ai/ollama.md](../06-ai/ollama.md) for the model choice rationale (4GB VRAM constraint).

## 8. Run tests

`TODO — PLANNED` — no test suite exists yet (see [14-testing/strategy.md](../14-testing/strategy.md)).

## 9. Access the application

`TODO — PLANNED` — no running application yet.

## Related documentation

- [Conventions](conventions.md)
- [Environments](../13-devops/environments.md)
- [Ollama](../06-ai/ollama.md)
