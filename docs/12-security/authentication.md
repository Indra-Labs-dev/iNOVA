# Authentication (Security View)

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

State the security requirements authentication must meet, complementing the implementation notes in [09-backend/authentication.md](../09-backend/authentication.md).

## Scope

Security requirements only — implementation choice lives in the backend doc.

## Requirements

- No plaintext credential storage under any circumstance.
- Session tokens must be revocable (logout must actually invalidate server-side state, not just clear a client token).
- Brute-force protection on login (rate limiting, see [network-security.md](network-security.md)).

## Related documentation

- [Backend authentication](../09-backend/authentication.md)
- [Secrets](secrets.md)
