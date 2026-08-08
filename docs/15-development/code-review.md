# Code Review

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define what a review must check before code merges, beyond "does it work."

## Scope

Review checklist.

## Checklist (once code exists)

- Matches the layering rules in [conventions.md](conventions.md) and the relevant architecture doc.
- Any new dependency justified per [dependency-policy.md](dependency-policy.md).
- Any new agent tool includes a permission/risk definition per [07-agents/permissions.md](../07-agents/permissions.md).
- Any security-relevant change (auth, permissions, secrets) gets explicit reviewer attention per [12-security/secure-development.md](../12-security/secure-development.md).
- Tests included for meaningful business logic (see [14-testing/strategy.md](../14-testing/strategy.md)).

## Related documentation

- [Conventions](conventions.md)
- [Secure development](../12-security/secure-development.md)
