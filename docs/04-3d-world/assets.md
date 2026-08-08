# Assets

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the 3D asset pipeline: format, sourcing, and optimization requirements.

## Scope

3D asset handling. Mascot animation assets are in [05-mascot/rive.md](../05-mascot/rive.md).

## Format

GLTF/GLB is the required format for all 3D models, per the product vision's explicit technology direction.

## Sourcing

- Custom modeling (e.g. Blender, free) for iNOVA-specific objects (mascot environment pieces, hub representations).
- Public asset libraries (Sketchfab, Poly Haven) for generic/placeholder objects during early development — license compliance must be checked per asset before shipping.

## Optimization checklist (apply before any asset is added to the repo)

- Polygon count appropriate for real-time rendering on the target device tier (see [performance.md](performance.md)).
- Texture sizes power-of-two, compressed where supported.
- Draco or equivalent mesh compression for larger models.
- No unused animations/materials baked into the exported file.

## Related documentation

- [Scene architecture](scene-architecture.md)
- [Performance](performance.md)
