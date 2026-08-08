# Authentication

**Status:** [IN PROGRESS] — approach decided ([ADR-0010](../adr/0010-authentication-approach.md)), Phase 0 scaffolding in progress
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how a user proves identity to iNOVA.

## Scope

AuthN only — see [authorization.md](authorization.md) for what an authenticated user can then do.

## Approach — decided

In-house: JWT access tokens (short-lived, HS256) + a PostgreSQL-backed `sessions` table holding hashed, rotating, revocable refresh tokens. Passwords hashed with Argon2id. See [ADR-0010](../adr/0010-authentication-approach.md) for the full analysis against the criteria below. Implemented from the first working version, never retrofitted (see [12-security/security-architecture.md](../12-security/security-architecture.md)).

Options and criteria retained below for record; the decision is final unless the trigger conditions in ADR-0010's Consequences section occur.

### Options

| Option | Pros | Cons |
|---|---|---|
| In-house (JWT + PostgreSQL-backed sessions) | No recurring cost, full control over session/permission model, no external dependency for a security-critical path | More implementation and maintenance burden (password hashing, token rotation, revocation, email verification flow all built by hand) |
| Managed provider (Auth0/Clerk/Firebase Auth) | Faster to implement, battle-tested against common auth vulnerabilities, handles email verification/MFA out of the box | Recurring cost at scale, external dependency for a security-critical path, less control over exact session/permission shape needed for [12-security/authorization.md](../12-security/authorization.md) |

### Decision criteria

- **Team size/velocity at Phase 0**: a solo/small team benefits more from a managed provider's speed; a team with backend security expertise can safely go in-house.
- **Budget tolerance**: see [iNOVA_CAHIER_DES_CHARGES.md §5.2](../../iNOVA_CAHIER_DES_CHARGES.md) — managed auth adds a recurring cost line the current local-LLM-driven budget plan doesn't assume.
- **Control requirement**: iNOVA's permission model ties directly into agent tool authorization ([07-agents/permissions.md](../07-agents/permissions.md)) — if a managed provider's session/claims model can't cleanly carry iNOVA's scoped permissions, in-house becomes preferable regardless of speed.
- **Timing**: this must be decided before Phase 0 scaffolding begins, since it shapes the `User`/`Session` entities ([10-data/entities.md](../10-data/entities.md)).

## Requirements

- Secure session handling, no plaintext credential storage.
- Account verification via email (see [integration-map.md](../02-architecture/integration-map.md) for the email provider dependency) — `[PLANNED]`, not part of Phase 0 (register/login/refresh/logout only; no email provider wired up yet).

## Related documentation

- [Authorization](authorization.md)
- [Security architecture](../12-security/security-architecture.md)
- [Secrets](../12-security/secrets.md)
