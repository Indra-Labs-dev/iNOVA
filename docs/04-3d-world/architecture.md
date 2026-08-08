# 3D World Architecture

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the internal structure of the iNOVA World 3D layer.

## Scope

Three.js/WebGL layer only. Integration with Flutter is in [2d-3d-integration.md](2d-3d-integration.md).

## Structure

```text
3D World
├── Scene
├── Camera
├── Renderer
├── Lighting
├── Assets
├── Models
├── Particles
├── Effects
├── Interactions
├── Events
└── Performance
```

## Principle

> The 3D layer is an experience layer, not the core business logic. It visualizes state that already exists elsewhere (in the backend, in Flutter state) — it never owns business state itself (see [02-architecture/overview.md](../02-architecture/overview.md)).

Do not build a large 3D environment before the underlying product (AI, data, agents) is functional — see [product-philosophy.md](../00-overview/product-philosophy.md) and [16-roadmap/phases.md](../16-roadmap/phases.md) (World is Phase 3, after AI Core).

## Gate 7 — first real increment (2026-08-08)

`frontend/lib/features/world/` implements the first non-spike piece of this structure: `Scene`,
`Camera`, `Renderer`, `Lighting` for one primitive (an icosahedron, colored from real Flutter
theme state), plus one `Events` case (object click → real navigation). `Assets`, `Models`,
`Particles`, `Effects`, and multi-object `Interactions` remain not started. See the [Gate 7
report](../16-roadmap/gate-7-first-3d-increment-report.md).

## Related documentation

- [Three.js](threejs.md)
- [WebGL](webgl.md)
- [Scene architecture](scene-architecture.md)
- [2D/3D integration](2d-3d-integration.md)
- [Performance](performance.md)
- [Gate 7 first 3D increment report](../16-roadmap/gate-7-first-3d-increment-report.md)
