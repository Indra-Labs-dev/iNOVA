# Secrets

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how credentials, API keys, and other secrets are handled.

## Scope

Secret lifecycle: storage, access, rotation.

## Rules

- Never committed to source control, under any circumstance — including in comments, example files, or test fixtures.
- Environment variables (or a dedicated secret manager, `TODO — decision required` on whether one is warranted at MVP scale) — never hard-coded.
- `.env` files (or equivalent) must be git-ignored from the first commit of the backend, not added reactively after a leak.
- CI/CD secrets scoped per environment (see [13-devops/ci-cd.md](../13-devops/ci-cd.md)).

## Related documentation

- [Security architecture](security-architecture.md)
- [Environments](../13-devops/environments.md)
