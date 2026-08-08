# Gate 7 Report — First Real 3D World Increment

**Status:** Complete
**Owner:** Archange Elie Yatte
**Date:** 2026-08-08

## Purpose

Two things, done as one Gate per the user's explicit GO:

1. Close the one real prerequisite the [Gate 6 spike report](gate-6-3d-spike-report.md) flagged
   but deliberately left open: Flutter's default web release build fetching CanvasKit and a
   font from `gstatic.com` — unrelated to Three.js, but a real violation of the project's
   "no external CDN, works offline" requirement for the whole app.
2. Build the first real (not spike) 3D World increment: one object, live in the actual app,
   colored from real Flutter state, whose click event triggers a real Flutter navigation.

## Part 1 — CanvasKit/font CDN fix

- `frontend/web/flutter_bootstrap.js` (new, project-root override) sets `canvasKitBaseUrl:
  "canvaskit/"`, pointing the loader at the CanvasKit build `flutter build web` already copies
  into `build/web/canvaskit/` — no download needed, it ships with the Flutter SDK.
- Roboto is now vendored as a real Flutter font asset (`frontend/fonts/roboto/`, official
  `google/fonts` repo, OFL 1.1 — see that directory's `PROVENANCE.md`), closing the base-text
  CDN fetch. No `ThemeData` change needed — Material 3's default `TextTheme` already references
  the `"Roboto"` family name.
- A second CDN fetch (Noto Sans Symbols, for glyphs outside Roboto's coverage) was traced to the
  `→`/`…`/`•` characters used in 4 already-shipped screens (Research, Missions, News, AI Chat).
  Confirmed with the user before touching shipped UI copy, then replaced with a local `Icon` or
  ASCII equivalent.
- **Verified**: `flutter build web --release`, served locally, `performance.getEntriesByType
  ('resource')` reports zero external requests on every screen checked. `flutter analyze` clean,
  21/21 tests still pass.
- **Residual, documented risk**: CanvasKit's `fontFallbackBaseUrl` still defaults to
  `fonts.gstatic.com` for any *future* glyph outside Roboto's coverage (emoji, CJK, etc.) — see
  [PROJECT_STATUS.md](../PROJECT_STATUS.md) "Known gaps".

## Part 2 — First real 3D increment

### Scope decisions, confirmed with the user before implementation

Per the Gate 6 report's own flag ("this is itself a small architecturally-significant decision
to present to you before writing it"), two product decisions were confirmed before writing code:

1. **Where does the scene live?** A new `/world` route reachable via a button from the home
   screen (same pattern as Research/Missions/News) — not a replacement of the home screen.
   Replacing the shell with the 3D world, per the target model in
   [navigation.md](../03-frontend/navigation.md), is a separate, larger decision for later.
2. **What does the click event do?** Navigates to Missions — chosen for fitting the
   exploration/gamification angle of the 3D world, and because Missions already has its own
   normal 2D entry point (satisfying [2d-3d-integration.md](../04-3d-world/2d-3d-integration.md)'s
   "every 3D interaction must also work identically from 2D UI" rule by construction).

### What was built

- `frontend/web/vendor/three/` — a second, permanent vendored copy of Three.js 0.180.0 (same
  source/version/license as the Gate 6 spike's copy, duplicated rather than shared so the spike
  stays independently deletable — see that directory's `PROVENANCE.md`).
- `frontend/web/world/world_bridge.js` — the real (non-spike) bridge: one icosahedron, a
  `setAccentColor(hex)` command (Flutter → Three.js), a click event (Three.js → Flutter), and a
  `bridgeVersion` ("1.0.0") checked at init — the first concrete instance of the versioned
  contract [2d-3d-integration.md](../04-3d-world/2d-3d-integration.md) calls for.
- `frontend/lib/features/world/` — `WorldScreen`, wired into the real `app_router.dart` as
  `AppRoutes.world` ('/world'), reachable via a "3D World →" button on `AiChatScreen`'s AppBar.
  The object's color comes from `Theme.of(context).colorScheme.primary` — real app state, never
  hardcoded in JS, per [architecture.md](../04-3d-world/architecture.md) "Principle". Clicking it
  calls `Navigator.pushNamed(context, AppRoutes.missions)`.

### A real finding during implementation: `flutter test` runs on the Dart VM, not web

Wiring `WorldScreen` into `app_router.dart` (imported by `main.dart`, imported by every test)
broke the entire test suite: `flutter test`'s default runner targets the Dart VM, which does not
have `dart:js_interop`, `dart:ui_web`, or `package:web` available at all — not "available but
broken," genuinely absent as a compilable library on that target. The Gate 6 spike never hit
this because its entrypoint (`lib/spike_3d_main.dart`) was never reachable from any test.

**Fix (the standard Flutter pattern for this, not a workaround):** conditional file export.
`world_screen.dart` is now:

```dart
export 'world_screen_stub.dart' if (dart.library.js_interop) 'world_screen_web.dart';
```

`world_screen_web.dart` holds the real implementation (identical to what was first written);
`world_screen_stub.dart` is a plain `Scaffold` saying the 3D World is web-only. `dart.library.
js_interop` resolves true only on web compile targets (dart2js/dart2wasm/ddc), false on the VM —
verified empirically both ways: `flutter test` now passes 21/21 with the stub selected, and a
fresh `flutter run`/`flutter build web --release` still renders the real Three.js scene, proving
the conditional correctly picks the web implementation there.

### Measurements (real, not estimated)

| Check | Result |
|---|---|
| `flutter analyze` | Clean |
| `flutter test` | 21/21 pass |
| Dev mode (`flutter run -d web-server`) | Scene renders, colored `0xFF0066FF` (the app's real `electricBlue` primary), rotates continuously, no console errors |
| Flutter → Three.js | Confirmed: theme color visibly applied to the object at init |
| Three.js → Flutter | Confirmed: clicking the object navigates to the real Missions screen (which shows its own sign-in gate, same as reached via 2D navigation) |
| Navigate away / back / re-enter | Clean: `dispose()` calls `jsDispose()` only, no `setState`; re-entering creates a fresh scene with no errors |
| `flutter build web --release`, served locally | Scene renders identically; `performance.getEntriesByType('resource')` reports **zero external requests**; `window.iNovaWorld.bridgeVersion === "1.0.0"` confirmed both sides |
| Click → Missions on the release build | Confirmed, same as dev mode |

### What this increment deliberately does not include

No map, no GLTF/GLB assets, no avatar, no Aira, no camera system beyond the fixed perspective
camera already used in the Gate 6 spike, no event bus, no multi-object scene, no backend
integration, no persistence. `04-3d-world/architecture.md`'s `Assets`, `Models`, `Particles`,
`Effects` remain not started. This is one object and one event, matching the Gate 6 report's
Gate 7 proposal scope exactly.

## Verdict

Both parts done and verified live: the CanvasKit/font prerequisite is closed (with one small,
documented residual risk for future non-Latin glyphs), and the first real 3D World increment
exists in the shipped app, colored by real Flutter state, with a real bidirectional bridge and a
real navigation consequence — not a spike, not a mock.

No ADR was written for 3D architecture — [ADR-0002](../adr/0002-threejs-3d-world.md) still
stands as the only accepted 3D decision; this Gate is an implementation of it, not a new
decision.

Per the gated plan, further 3D World expansion (more objects, real scene content, GLTF, Aira,
event bus, or replacing the home screen with the 3D world) requires its own explicit GO.

## Related documentation

- [Gate 6 3D spike report](gate-6-3d-spike-report.md)
- [2D/3D Integration](../04-3d-world/2d-3d-integration.md)
- [3D World Architecture](../04-3d-world/architecture.md)
- [Navigation](../03-frontend/navigation.md)
- [PROJECT_STATUS.md](../PROJECT_STATUS.md)
