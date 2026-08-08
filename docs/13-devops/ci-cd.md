# CI/CD

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the automated pipeline that verifies and ships changes.

## Scope

CI/CD tooling and pipeline stages.

## Tooling

GitHub Actions, given the repository is hosted on GitHub (`Indra-Labs-dev/iNOVA`) — free tier is sufficient at this project's current scale (see [iNOVA_CAHIER_DES_CHARGES.md §5.2](../../iNOVA_CAHIER_DES_CHARGES.md)).

## Target pipeline stages (once code exists)

```text
Lint → Unit tests → Integration tests → Build → (Deploy on merge to main, staging first)
```

See [14-testing/strategy.md](../14-testing/strategy.md) for what each test stage covers.

## Status note

No workflow file exists yet — nothing to run CI against.

## Related documentation

- [Testing strategy](../14-testing/strategy.md)
- [Deployment](deployment.md)
