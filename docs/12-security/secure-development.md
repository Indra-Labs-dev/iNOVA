# Secure Development

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define development-process practices that keep security from being an afterthought.

## Scope

Process, not runtime architecture.

## Practices

- Dependency updates tracked, no unjustified new dependencies (see [15-development/dependency-policy.md](../15-development/dependency-policy.md)).
- Security-relevant changes (auth, permissions, agent tools) require explicit review attention (see [15-development/code-review.md](../15-development/code-review.md)).
- Security test category exists and runs before release (see [14-testing/security-tests.md](../14-testing/security-tests.md)).

## Related documentation

- [Dependency policy](../15-development/dependency-policy.md)
- [Code review](../15-development/code-review.md)
- [Security tests](../14-testing/security-tests.md)
