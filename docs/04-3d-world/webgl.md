# WebGL

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Document WebGL-level constraints that the 3D world must respect.

## Scope

Rendering-layer concerns underneath Three.js.

## Constraints to document once implemented

- Minimum supported WebGL version (target: WebGL2, with a documented fallback or graceful degradation path for WebGL1-only devices — decision `TODO — decision required` once real device targets are known).
- GPU memory budget for the world scene, coordinated with [performance.md](performance.md).
- Context-loss handling (WebGL contexts can be lost on tab backgrounding/GPU resets) — the world must recover without crashing the Flutter shell.

## Related documentation

- [Three.js](threejs.md)
- [Performance](performance.md)
