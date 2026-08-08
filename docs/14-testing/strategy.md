# Testing Strategy

**Status:** [PLANNED] — no test suite exists yet
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define what layers of testing iNOVA needs and in what order they run.

## Scope

Entry point for `14-testing/`. Each layer has its own document.

## Pyramid

```text
Unit
 ↓
Integration
 ↓
API
 ↓
Frontend
 ↓
Agent
 ↓
Security
 ↓
E2E
```

## Before each release (target gate, once a release process exists)

- All unit and integration tests pass.
- API contract tests pass.
- Agent permission/tool-call validation tests pass (see [agent-tests.md](agent-tests.md)) — non-negotiable given the security model in [12-security/agent-security.md](../12-security/agent-security.md).
- Security test suite passes (see [security-tests.md](security-tests.md)).
- No regressions in core E2E journeys (see [16-roadmap/mvp.md](../16-roadmap/mvp.md) for what "core" means at each phase).

## Related documentation

- [Unit tests](unit-tests.md)
- [Agent tests](agent-tests.md)
- [Security tests](security-tests.md)
