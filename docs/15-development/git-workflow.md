# Git Workflow

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how changes flow into `main` on `Indra-Labs-dev/iNOVA`.

## Scope

Git process. Branch naming is in [branching.md](branching.md).

## Current state

Single `main` branch, one commit so far. No enforced PR process yet — appropriate to formalize once more than one contributor is active.

## Target workflow

Feature branches → PR → review (see [code-review.md](code-review.md)) → merge to `main`. CI (once it exists, see [13-devops/ci-cd.md](../13-devops/ci-cd.md)) must pass before merge.

## Related documentation

- [Branching](branching.md)
- [Code review](code-review.md)
