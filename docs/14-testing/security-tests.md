# Security Tests

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Verify the security invariants in [12-security/](../12-security/security-architecture.md) actually hold.

## Scope

Authorization bypass attempts, input validation, secret handling.

## Required coverage before any release

- Attempt to access another user's data → must be denied.
- Attempt to call a tool without the required permission → must be denied.
- Attempt to submit malformed/oversized input to any endpoint → must be rejected cleanly, not crash the service.
- Verify no secrets appear in logs or error responses (see [12-security/secrets.md](../12-security/secrets.md)).

## Related documentation

- [Strategy](strategy.md)
- [Threat model](../12-security/threat-model.md)
- [Agent tests](agent-tests.md)
