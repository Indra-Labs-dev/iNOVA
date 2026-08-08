# Dependency Policy

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Prevent dependency sprawl, per the explicit instruction not to install dozens of dependencies without justification.

## Scope

Applies to both Flutter (`pubspec.yaml`) and Python (`requirements.txt`/`pyproject.toml`) dependencies.

## Rule

A new dependency requires a stated reason beyond "it's convenient" — specifically, what it replaces or what capability doesn't already exist in the stack described in [02-architecture/overview.md](../02-architecture/overview.md). Prefer the standard library or an already-adopted library over adding a new one for a marginal gain.

## Related documentation

- [Conventions](conventions.md)
- [Code review](code-review.md)
