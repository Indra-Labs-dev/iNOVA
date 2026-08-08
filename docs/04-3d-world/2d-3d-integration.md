# 2D/3D Integration

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the contract between the Flutter shell and the Three.js world so they stay decoupled.

## Scope

The bridge layer only.

## Integration model

The 3D world runs embedded (web: canvas/WebView interop; other targets: platform-appropriate embedding) and communicates with Flutter exclusively through a typed event bridge — never through shared mutable state.

```mermaid
graph LR
    Flutter -->|navigation intent, theme, events| Bridge[Event Bridge]
    Bridge -->|scene commands| ThreeJS[Three.js World]
    ThreeJS -->|object clicked, camera ready| Bridge
    Bridge -->|navigation triggered| Flutter
```

## Rules

- Flutter never reaches into Three.js internals directly, and vice versa — only bridge messages.
- The bridge protocol is versioned and documented here once implemented, to avoid silent breakage between the two layers.
- Every 3D interaction that changes app state (e.g. navigating to a hub) must also work identically from the 2D UI — the 3D world is never the only path to a feature (see [performance.md](performance.md) fallback requirement).

## Gate 6 spike findings (2026-08-08)

An isolated feasibility spike validated the mechanical half of this contract: a Flutter
`HtmlElementView` hosting a Three.js scene, with commands flowing Flutter → Three.js (via
`dart:js_interop` calling into a small `three_bridge.js`) and events flowing Three.js → Flutter
(via a JS callback into Dart), both proven live and repeatedly, including in a `--release`
build. The spike did not implement the versioned bridge protocol or a navigation-triggering
event — see [Gate 6 report](../16-roadmap/gate-6-3d-spike-report.md) for measurements and the
Gate 7 proposal, which would be the first Gate to exercise this document's "navigation triggered"
rule for real. Status here stays `[PLANNED]`.

## Related documentation

- [Architecture](architecture.md)
- [Navigation](../03-frontend/navigation.md)
- [Performance](performance.md)
- [Gate 6 3D spike report](../16-roadmap/gate-6-3d-spike-report.md)
