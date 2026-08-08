# ADR-0002: Three.js/WebGL for the 3D world

**Status:** Accepted
**Date:** 2026-08-08

## Context

iNOVA World ([04-3d-world/](../04-3d-world/architecture.md)) needs a web-native 3D rendering technology that embeds inside a Flutter web app without requiring a separate native engine runtime.

## Decision

Three.js over WebGL is the 3D engine, using GLTF/GLB assets. This is treated as non-negotiable: do not replace it with Unity or another engine unless a future ADR explicitly supersedes this one.

## Consequences

- Runs natively in-browser, no plugin/runtime install required for users.
- Large, well-maintained ecosystem (loaders, post-processing) reduces custom low-level WebGL code.
- Requires the 2D/3D integration bridge documented in [04-3d-world/2d-3d-integration.md](../04-3d-world/2d-3d-integration.md) since Flutter doesn't natively host Three.js.
- Performance is bounded by WebGL/browser constraints and the user's device — see [04-3d-world/performance.md](../04-3d-world/performance.md) fallback requirement.

## Alternatives considered

- Unity (WebGL export) — heavier runtime, worse integration with a Flutter shell, rejected for the web-first MVP.
- A native game engine per platform — abandons the "one experience across platforms" goal.
