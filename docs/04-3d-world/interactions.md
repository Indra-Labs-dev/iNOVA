# Interactions

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how users interact with the 3D world (camera control, object selection, navigation triggers).

## Scope

Input handling and navigation semantics within the 3D scene.

## Planned interactions

- Camera navigation (orbit/pan, constrained to avoid disorientation) to move between hub representations.
- Clicking/tapping a hub representation triggers the same navigation as its 2D nav equivalent (see [03-frontend/navigation.md](../03-frontend/navigation.md)).
- Hover/focus states on interactive 3D objects mirror 2D affordances (cursor change, subtle highlight) for consistency.

## Related documentation

- [Scene architecture](scene-architecture.md)
- [2D/3D integration](2d-3d-integration.md)
- [Navigation](../03-frontend/navigation.md)
