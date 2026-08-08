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

## Gate 6 spike findings (2026-08-08)

A feasibility spike (isolated, not the real 3D World — see
[Gate 6 report](../16-roadmap/gate-6-3d-spike-report.md)) measured that Flutter Web can host and
drive Three.js/WebGL with reliable bidirectional communication using native `dart:js_interop` +
`dart:ui_web` + a vendored (MIT, npm-sourced) `three@0.180.0` build — no Three.js wrapper
package, no CDN for the engine itself. Verdict: READY for that specific question. A separate,
Flutter-platform-level finding (CanvasKit/font CDN fetch in `--release` builds, unrelated to
Three.js) remains unresolved and is a prerequisite for the first real 3D Gate — see the report
for detail. Status here stays `[PLANNED]`: this is measurement evidence, not the implementation.

## Usage guidelines

- Prefer built-in Three.js primitives and well-maintained addons (e.g. `GLTFLoader`, post-processing composer) over custom low-level WebGL code, except where performance profiling proves it necessary.
- Scene code lives isolated from Flutter widget code (see [scene-architecture.md](scene-architecture.md)) and communicates only via the event bridge described in [2d-3d-integration.md](2d-3d-integration.md).

## Related documentation

- [WebGL](webgl.md)
- [Scene architecture](scene-architecture.md)
- [Assets](assets.md)
