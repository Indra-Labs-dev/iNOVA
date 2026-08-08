# Accessibility

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Ensure the futuristic visual identity never comes at the cost of usability for all users.

## Scope

Cross-cutting accessibility requirements for 2D UI, 3D world, and mascot.

## Requirements

- Respect OS/browser-level "reduce motion" settings: disable non-essential 3D camera motion, particle effects, and mascot idle animations when set (see [04-3d-world/performance.md](../04-3d-world/performance.md), [05-mascot/animation-guidelines.md](../05-mascot/animation-guidelines.md)).
- Maintain WCAG AA contrast minimums even within glass/holographic UI treatments (see [design-system.md](design-system.md)).
- All interactive elements reachable and operable via keyboard, independent of 3D world state.
- Screen-reader labeling for mascot state changes (e.g. an error state must be announced, not just visually shown).

## Related documentation

- [Design system](design-system.md)
- [Responsive design](responsive-design.md)
- [Non-functional requirements](../01-product/non-functional-requirements.md)
