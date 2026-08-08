# Flutter

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Record how and why Flutter is used as iNOVA's primary frontend, and the platform targets it must support.

## Scope

Flutter-specific concerns. See [adr/0001-flutter-frontend.md](../adr/0001-flutter-frontend.md) for the decision rationale.

## Target platforms

Web-first (primary target for MVP), with the same codebase intended to later support desktop and mobile builds without a rewrite — this is one of the reasons Flutter was chosen over a web-only framework.

## Responsibilities

Flutter owns: application shell, navigation, 2D interface, dashboards, forms, settings, cards, data views, responsive layout, REST API integration, WebSocket integration. It embeds — but does not implement — the 3D layer (see [2d-3d-integration.md](../04-3d-world/2d-3d-integration.md)).

## Conventions

- Null-safety enforced throughout.
- Widgets kept small; screen-level widgets compose smaller feature widgets rather than growing monolithically (see [architecture.md](architecture.md)).
- No direct HTTP calls from widgets — always through a repository/service layer wired via Riverpod (see [riverpod.md](riverpod.md)).

## Related documentation

- [Architecture](architecture.md)
- [Riverpod](riverpod.md)
- [Responsive design](responsive-design.md)
