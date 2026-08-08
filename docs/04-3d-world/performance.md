# Performance

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Set the performance bar and fallback behavior for the 3D world, so it never becomes the bottleneck of the whole product.

## Scope

3D-specific performance. General non-functional performance targets are in [01-product/non-functional-requirements.md](../01-product/non-functional-requirements.md).

## Requirements

- Target frame rate: `TODO — decision required` once real scenes exist to profile (aim for a stable 60fps on mid-range hardware, degrading gracefully rather than dropping frames unpredictably).
- Lazy loading of scene assets — the initial app load must not block on 3D asset downloads.
- Level of detail (LOD) for complex models, if/when scene complexity requires it — not needed at MVP scene complexity.
- GPU memory budget monitored explicitly given that development itself happens on constrained hardware (see [06-ai/model-strategy.md](../06-ai/model-strategy.md) for the equivalent AI-side constraint).

## Fallback behavior

When the 3D world is unavailable or underperforming (low-end device, WebGL unsupported, reduced-motion preference), iNOVA must fall back to a 2D-only experience without losing functionality — the 3D world is additive, never a hard dependency for using the product (see [2d-3d-integration.md](2d-3d-integration.md)).

## Related documentation

- [Scene architecture](scene-architecture.md)
- [2D/3D integration](2d-3d-integration.md)
- [Accessibility](../03-frontend/accessibility.md)
