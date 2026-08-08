# Scope

**Document status:** Living document — update every phase
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Prevent the single most common failure mode of this project: conflating what iNOVA is *meant to become* with what it *currently is*. Every reader of this documentation set must be able to tell these apart at a glance.

## The three layers

```text
PRODUCT VISION
     |
ARCHITECTURE TARGET
     |
CURRENT IMPLEMENTATION
```

- **Product vision** — described in [vision.md](vision.md), the original `iNOVA_MASTER_CONTEXT.md`, and `iNOVA_OBJECTIFS_FONCTIONNALITES_STACK.md` at the repository root. This is aspirational and long-lived; it does not imply anything is built.
- **Architecture target** — described throughout `docs/02-architecture/` through `docs/14-testing/`. This is the intended design for each system once built, regardless of whether it exists yet.
- **Current implementation** — described exclusively in [PROJECT_STATUS.md](../PROJECT_STATUS.md), and via inline `[STATUS]` labels used throughout this documentation set. This is the only place that reflects the actual state of the repository.

**Rule:** never present a planned feature as implemented. Use these labels consistently across all documents:

```text
[NOT STARTED]
[PLANNED]
[IN PROGRESS]
[PARTIAL]
[IMPLEMENTED]
[TESTED]
[STABLE]
[DEPRECATED]
```

If a fact is not yet known or decided, write `TODO — decision required` rather than inventing an answer.

## Current scope status (2026-08-08)

The repository currently contains **no application code**. It contains:

- Product vision documents (`iNOVA_MASTER_CONTEXT.md`, `iNOVA_CAHIER_DES_CHARGES.md`, `iNOVA_OBJECTIFS_FONCTIONNALITES_STACK.md`).
- This `docs/` technical and product documentation set.
- Brand assets (`logo.png`, `mascotte-aira.png`).

Every module and system described in this documentation is therefore `[PLANNED]` unless [PROJECT_STATUS.md](../PROJECT_STATUS.md) says otherwise. See that file for the authoritative, up-to-date table.

## What is explicitly out of scope for now

Per [product-philosophy.md](product-philosophy.md) and the [roadmap](../16-roadmap/roadmap.md), the following are not being built yet and should not be started opportunistically:

- Full 3D world beyond an initial scene.
- All nine specialized agents at once (start with `ResearchAgent`).
- Learning Hub, Productivity Hub, Device Hub, Cloud Hub (Phase 7).
- Any feature whose only justification is "it's in the vision document."

## Related documentation

- [PROJECT_STATUS.md](../PROJECT_STATUS.md)
- [Roadmap](../16-roadmap/roadmap.md)
- [Feature matrix](../01-product/feature-matrix.md)
