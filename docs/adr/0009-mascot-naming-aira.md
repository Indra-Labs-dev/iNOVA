# ADR-0009: Mascot naming — Aira

**Status:** Accepted
**Date:** 2026-08-08

## Context

The first documentation pass used "Nova" as a working name for iNOVA's AI mascot throughout `05-mascot/` and cross-references elsewhere, while a concept asset already present in the repository (`mascotte-aira.png`) suggested "Aira." This was flagged as an open naming question in the initial review rather than guessed.

## Decision

The mascot/AI companion is officially named **Aira**. The product name remains **iNOVA**. The two are never interchangeable:

```text
Product:      iNOVA
AI Companion: Aira
```

Aira is a character/companion integrated into the iNOVA ecosystem, not an alternate product name, and must never be used as one (e.g. never "Aira" as a marketing name for the platform itself).

## Consequences

- All mascot-context documentation updated from "Nova" to "Aira" (05-mascot/, relevant cross-references in 00-overview, 01-product, 02-architecture, 07-agents, 16-roadmap, PROJECT_STATUS.md, README.md, and ADR-0003).
- The `Nova*` UI component prefix in [03-frontend/design-system.md](../03-frontend/design-system.md) (`NovaCard`, `NovaButton`, etc.) is a separate design-token naming convention, not the mascot's identity — left unchanged pending its own decision (see that document's naming note). This ADR does not resolve that question.
- Occurrences of "iNOVA" (the product name) are explicitly untouched by this decision.

## Alternatives considered

- Keeping "Nova" as the mascot name — rejected: contradicts the explicit product decision and the pre-existing concept asset naming, and risks confusion with the product name "iNOVA" (a near-homophone), which "Aira" avoids.
