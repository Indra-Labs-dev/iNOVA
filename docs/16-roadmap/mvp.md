# MVP

**Status:** [PLANNED] — not started
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the smallest slice that proves iNOVA's central concept before any further expansion.

## Scope

MVP-only feature set, cross-referencing [01-product/feature-matrix.md](../01-product/feature-matrix.md) for full-product context.

## MVP goal

> AI + Agent + Data + Aira (mascot) + 2D/3D interface can operate as one coherent experience.

The MVP is a **vertical slice**, not a horizontal completion of early roadmap phases before later ones start. It deliberately includes thin slices of modules whose full version is scheduled later (Agent Hub, News Intelligence, Cybersecurity Hub, Mission System) — see [16-roadmap/phases.md](phases.md) "How MVP relates to these phases" for exactly which slice of each. This is intentional, not a phase-dependency error.

## MVP scope

```text
iNOVA MVP
|
+-- AI Companion — chat, basic memory, tool system
+-- Futuristic Dashboard — 2D UI, initial 3D world
+-- Aira (Mascot) — Rive, basic emotional states (idle, thinking, speaking, success, error)
+-- Agent Hub — ResearchAgent only
+-- News Intelligence — RSS/API ingestion, AI summarization
+-- Basic Security Hub — security posture, recommendations
+-- Missions — simple tasks, XP
```

## Explicitly excluded from MVP

The MVP must not attempt to build, in parallel:

- All nine agents (only `ResearchAgent` is in scope).
- The full Cybersecurity Hub (CVE lookup, file analysis, URL/domain reputation, `CyberAgent`).
- The full Programming Hub (Monaco editor, Git/GitHub integration, `CodeAgent`).
- The OSINT system (`OSINTAgent`, DNS/certificate/domain intelligence).
- The full Learning Hub platform (`TutorAgent`, courses, adaptive difficulty).
- The full Productivity Hub platform (`ProductivityAgent`, calendar, habits).
- The full Cloud/Infrastructure Hub (`CloudAgent`, Docker/server management).
- The full 3D world (only an initial scene with basic navigation is in scope).
- Knowledge Graph, advanced Watchlists, iNOVA Pulse, Device Hub.

See [00-overview/scope.md](../00-overview/scope.md) and [16-roadmap/phases.md](phases.md) for what each of these becomes once its own phase is reached.

## Success criteria

- User can chat with the AI, which can invoke at least one real tool in an audited, permissioned way.
- The mascot visibly reacts to at least 3 states.
- The 3D world loads and allows basic navigation to 2D modules.
- `ResearchAgent` executes an end-to-end task with a visible execution trace.
- No hardcoded secrets, working authentication, server-side permission checks.

## Related documentation

- [Roadmap](roadmap.md)
- [Phases](phases.md)
- [Cahier des charges §2](../../iNOVA_CAHIER_DES_CHARGES.md)
