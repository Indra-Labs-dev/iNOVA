# Three.js

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Record the decision and constraints around using Three.js as the 3D engine.

## Scope

Engine-level concerns. See [adr/0002-threejs-3d-world.md](../adr/0002-threejs-3d-world.md) for rationale.

## Decision

Three.js is an explicit, non-negotiable architectural decision (per the product vision). Do not replace it with Unity or another engine unless a future ADR explicitly supersedes this one.

## Usage guidelines

- Prefer built-in Three.js primitives and well-maintained addons (e.g. `GLTFLoader`, post-processing composer) over custom low-level WebGL code, except where performance profiling proves it necessary.
- Scene code lives isolated from Flutter widget code (see [scene-architecture.md](scene-architecture.md)) and communicates only via the event bridge described in [2d-3d-integration.md](2d-3d-integration.md).

## Related documentation

- [WebGL](webgl.md)
- [Scene architecture](scene-architecture.md)
- [Assets](assets.md)
