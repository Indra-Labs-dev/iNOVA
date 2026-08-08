# Navigation

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how users move between the 2D shell and the 3D world, and between hubs.

## Scope

Navigation architecture only; the 3D navigation experience itself is in [04-3d-world/interactions.md](../04-3d-world/interactions.md).

## Model

- A single root navigator manages top-level routes: auth, main shell, settings.
- Within the shell, each hub is a nested route (`/ai`, `/agents`, `/security`, ...), consistent with the `features/` structure in [architecture.md](architecture.md).
- The 3D world is not a route by itself — it's a navigable visual layer that can trigger the same route transitions as clicking a 2D nav item (see [2d-3d-integration.md](../04-3d-world/2d-3d-integration.md)).

## Deep linking

Every hub route should be deep-linkable (e.g. sharing a link to a specific mission or news digest) — this is a target requirement, not yet implemented.

## Related documentation

- [Architecture](architecture.md)
- [2D/3D integration](../04-3d-world/2d-3d-integration.md)
- [Responsive design](responsive-design.md)
