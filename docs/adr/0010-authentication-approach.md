# ADR-0010: Authentication approach — in-house JWT + revocable sessions

**Status:** Accepted
**Date:** 2026-08-08

## Context

[09-backend/authentication.md](../09-backend/authentication.md) left the authentication approach open with two options: in-house (JWT + PostgreSQL-backed sessions) vs. a managed provider (Auth0/Clerk/Firebase Auth). Phase 0 Foundation requires this resolved before the initial `User`/`Session` schema is created, since it shapes those entities.

## Analysis against the stated criteria

| Criterion | In-house (JWT + PostgreSQL sessions) | Managed provider (Auth0/Clerk/Firebase) |
|---|---|---|
| Security | Correct if implemented with modern primitives (Argon2id hashing, short-lived access tokens, revocable refresh tokens) — no shortcuts taken here | Very strong out of the box, audited by a specialized vendor |
| Simplicity | More code to write now (register/login/refresh), but the surface is small and well-understood | Fastest to stand up |
| Cost | No recurring cost — consistent with the local-LLM cost-minimization decision already made ([ADR-0005](0005-ollama-local-llm.md)) and the single-VPS budget target ([iNOVA_CAHIER_DES_CHARGES.md §5.6](../../iNOVA_CAHIER_DES_CHARGES.md)) | Recurring cost at scale; a second billed external dependency alongside hosting |
| Control | Full — session/claims shape can be designed to carry iNOVA's scoped permissions directly ([07-agents/permissions.md](../07-agents/permissions.md)) | Limited — third-party claims format needs a mapping layer to iNOVA's permission model |
| Extensibility | Good — MFA, additional claims, or a future managed-provider migration can be added without a foundational rewrite | Good for auth itself, weaker for permission-model integration |
| Flutter integration | Standard bearer-token pattern, `flutter_secure_storage` for token storage | Official SDKs available, comparable effort |
| FastAPI integration | Standard `OAuth2PasswordBearer` + JWT pattern, extensively documented | Requires JWKS verification setup, more moving parts |
| Session management | Explicit, revocable refresh-token table under our control — matches the "sessions must be revocable" requirement in [12-security/authentication.md](../12-security/authentication.md) | Handled by the vendor, but as an opaque dependency |
| Future MFA | Addable as an extra verification step later, no architectural change required | Available out of the box today — the strongest point in its favor |
| Maintenance | Ongoing responsibility for a security-critical path, but the current team (single author) and stack are simple enough to carry it correctly | Low maintenance, but adds vendor lock-in risk for a security-critical path |

## Decision

Build authentication in-house: JWT access tokens (short-lived, HS256, signed with a server-held secret) + a PostgreSQL-backed `sessions` table holding hashed, rotating refresh tokens with explicit revocation support. Passwords hashed with Argon2id.

This is not chosen because it is popular — it is chosen because it is the only option that avoids adding a recurring-cost external dependency this early, while giving full control over the claims shape the agent permission model ([ADR-0007](0007-agent-permissions.md)) will need to consume later.

## Consequences

- No recurring auth billing at MVP scale.
- The team owns password-reset, MFA, and account-recovery flows when they're needed — none of these are built in Phase 0 beyond register/login/refresh/logout.
- Session claims can be shaped from day one to carry permission scopes cleanly.
- If the team grows significantly or compliance requirements demand vendor-audited auth, revisit this ADR — the in-house implementation does not block a future migration, but that migration was not designed for in this pass.

## Alternatives considered

- Auth0/Clerk/Firebase Auth — rejected for now on cost and control grounds, not on security grounds; remains a valid future option if the trigger conditions above occur.
