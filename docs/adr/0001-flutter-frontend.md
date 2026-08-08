# ADR-0001: Flutter as primary frontend

**Status:** Accepted
**Date:** 2026-08-08

## Context

iNOVA needs a single frontend codebase that can plausibly target web (primary at MVP), and later desktop/mobile, without a rewrite — while supporting a rich, animated, custom design system ([03-frontend/design-system.md](../03-frontend/design-system.md)) and hosting an embedded 3D layer ([04-3d-world/](../04-3d-world/architecture.md)).

## Decision

Flutter (Dart) is the primary frontend framework, with Riverpod for state management (see [03-frontend/riverpod.md](../03-frontend/riverpod.md)).

## Consequences

- One codebase, multiple future targets (web/desktop/mobile) without a rewrite.
- Strong typing and widget composition suit the "small, cohesive components" principle ([00-overview/product-philosophy.md](../00-overview/product-philosophy.md)).
- Embedding a WebGL/Three.js layer inside Flutter requires a deliberate integration boundary (see [04-3d-world/2d-3d-integration.md](../04-3d-world/2d-3d-integration.md)) rather than native browser DOM/canvas ownership a pure web framework would have.
- Team/contributors need Dart/Flutter familiarity.

## Alternatives considered

- A pure web framework (React/Vue) — faster native integration with Three.js, but no credible path to native mobile/desktop from the same codebase without significant duplication.
- Unity for the whole app — rejected; Unity is explicitly reserved for a possible future 3D-engine change only, not the primary app shell (see [ADR-0002](0002-threejs-3d-world.md)).
