# Scene Architecture

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how the 3D world's scene graph is organized as more modules get visual representations.

## Scope

Scene composition. Asset pipeline is in [assets.md](assets.md).

## Concept

```text
                 iNOVA WORLD

                     NOVA

        Cyber             AI
          |               |
       Security         Intelligence

     Code                 Agents

       Learning         Productivity
```

The 3D world can contain: a central planet/world, futuristic buildings per hub, holographic interfaces, portals, particle systems, floating objects, data streams, and visual representations of each module.

## Guideline

- Start with a minimal scene (Phase 3 target): one navigable scene with placeholder representations for the modules that exist at that point, not the full concept diagram above.
- Each hub's visual representation is added only once that hub itself reaches `[IN PROGRESS]` — avoid building 3D assets for modules that don't exist yet (see [scope.md](../00-overview/scope.md)).

## Related documentation

- [Architecture](architecture.md)
- [Assets](assets.md)
- [Interactions](interactions.md)
