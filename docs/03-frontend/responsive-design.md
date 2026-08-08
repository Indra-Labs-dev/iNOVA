# Responsive Design

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how iNOVA adapts across mobile, tablet, and desktop/web viewports.

## Scope

Layout behavior. Visual tokens are in [design-system.md](design-system.md).

## Breakpoint strategy

`[PLANNED]` — target breakpoints: mobile (<600px), tablet (600–1024px), desktop (>1024px). To be finalized once the first real screens are built rather than guessed in the abstract.

## Principles

- The 3D world is the first thing to degrade or hide on low-end/mobile devices — see [04-3d-world/performance.md](../04-3d-world/performance.md) and its fallback behavior.
- Dashboards reflow to single-column below tablet width; no horizontal scroll for primary content.
- Mascot presence scales down (smaller, less animation-heavy) on constrained viewports.

## Related documentation

- [Design system](design-system.md)
- [3D performance](../04-3d-world/performance.md)
- [Accessibility](accessibility.md)
