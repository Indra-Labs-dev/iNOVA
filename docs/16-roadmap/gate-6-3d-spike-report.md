# Gate 6 Report — 3D World Feasibility Spike

**Status:** Complete
**Owner:** Archange Elie Yatte
**Date:** 2026-08-08

## Purpose

Answer one question with real, measured evidence before any real 3D World code is written:
**can Flutter Web host and drive a Three.js/WebGL scene with reliable bidirectional
communication, fully locally (no external CDN for the 3D layer), including in a production
(`--release`) build?**

This is a spike, not the real 3D World. No map, no GLTF/GLB assets, no avatar, no Aira, no
navigation into other modules, no camera system, no event bus, no backend, no persistence, no
business logic. Everything below is isolated to `frontend/lib/spike_3d/`,
`frontend/web/spike3d/`, and `frontend/lib/spike_3d_main.dart` — deletable by removing those
three paths plus the `web: ^1.1.0` line in `pubspec.yaml`, with zero change to any shipped
feature (Chat, Conversations, Research, Missions, News, Auth, backend).

## 1. Does the spike work or fail?

**It works.** A rotating cube renders inside a Flutter-hosted `HtmlElementView`, driven by
Three.js/WebGL, with both communication directions proven live, repeatedly, including against
the `flutter build web --release` output served without a dev server.

- **Flutter → Three.js**: dragging the Flutter `Slider` calls `jsSetRotationSpeed(value)` via
  `dart:js_interop`; the cube's rotation speed changes immediately (confirmed live at
  `rotation speed = 0.132`).
- **Three.js → Flutter**: clicking the cube in the WebGL canvas fires a raycaster hit in
  `three_bridge.js`, which calls back into Dart through a `JSFunction` callback; the Flutter
  panel updates with `Cube clicked at 6:51 PM (JS performance.now()=260329.2ms)`.
- **Isolation**: `flutter analyze` stays clean and the main app's `flutter test` suite stays at
  21/21 passing with the spike present — no shipped file was touched.

## 2. Measurements (real, not estimated)

Where a metric could not be captured cleanly with the tools available in this environment, that
is stated explicitly below rather than filled in with a guess.

| Metric | Result | How it was captured |
|---|---|---|
| Initial load timeline | `three_bridge.js` loaded at +310ms, `iNovaSpike3D.init()` called and scene ready at +403ms after screen build, against the served `--release` build | In-app log panel, timestamped against `DateTime.now()` from screen `initState()` |
| FPS | 60 FPS, stable | `three_bridge.js`'s own frame counter (`getFps()`), polled every 1s and displayed in the Flutter panel |
| Flutter → Three.js latency | Not cleanly measurable with the tools available here | The command applies within the same animation frame (no dropped frames observed at 60 FPS while dragging), but no dedicated timer instrumented the call boundary — reported as "no perceptible lag," not as a number, to avoid presenting an estimate as a measurement |
| Three.js → Flutter latency | Not cleanly measurable with the tools available here | Same reason — the click-to-panel-update was visually instantaneous across repeated tests, but nothing timestamped the JS-callback-to-`setState` boundary specifically |
| Memory | Not measured | No reliable in-environment tool for JS heap / WebGL memory sampling was available; not reported rather than fabricated |
| Behavior after navigation away | Clean: `dispose()` cancels the FPS timer and calls `jsDispose()` (cancels the animation frame, removes listeners, disposes the WebGL renderer); back button returns to the spike's own menu screen with zero console errors | `read_console_messages` checked after navigating back, in a fresh tab to avoid a stale buffer |
| Behavior after returning to the screen | Re-initializes cleanly: new `HtmlElementView` instance, new container div polled and found, `iNovaSpike3D.init()` called again, fresh load timeline and working bridge | Repeated navigate-away/navigate-back cycle, verified via DOM/log inspection |
| Behavior after reload | Resets to the spike's menu route, not the 3D screen — Flutter Web's default single-entrypoint routing behavior for this spike (no deep-link route was implemented, since routing isn't part of what's under test) | Direct reload, confirmed via `document.title`/route state inspection |
| `flutter build web --release` | Succeeds, 74.0s | Direct build invocation |
| Release bundle size | `main.dart.js`: 2,075,037 bytes; `spike3d/` static assets (vendored Three.js + bridge script): 732 KB | `ls -la` / `du` on the build output before cleanup |
| Release build served and tested | Full interactive re-verification (load timeline, FPS, slider, cube click, navigation) repeated against `python3 -m http.server` serving the actual `--release` output, not just `flutter run -d chrome` | Screenshots + `performance.getEntriesByType('resource')` |

## 3. Problems encountered (all real, all documented as found)

1. **Missing companion file in the vendored Three.js build.** `three.module.min.js` (0.180.0)
   has an internal ES module `import` of `./three.core.min.js` — the build splits core
   math/object code into a separate chunk. Only the first file was vendored initially, causing
   a real runtime failure (`FAILED to load three_bridge.js: Bad state: ...`). Diagnosis was
   harder than a normal 404 because Flutter's dev server (`flutter run -d web-server`) returns
   HTTP 200 with `index.html`'s SPA-fallback content for unknown paths instead of a 404 —
   confirmed directly with `curl`. Fixed by vendoring `three.core.min.js` from the same npm
   tarball; documented in
   [`frontend/web/spike3d/vendor/three/PROVENANCE.md`](../../frontend/web/spike3d/vendor/three/PROVENANCE.md).
2. **`dispose()` calling `setState()`.** Navigating away from the spike screen initially threw
   `Assertion failed: _lifecycleState != _ElementLifecycle.defunct`, because the original
   `dispose()` logged a "screen disposed" line through `_appendLog()`, which calls `setState()`
   after the widget had already begun unmounting. Caught by the spike's own navigate-away test,
   exactly the kind of bug this exercise exists to surface. Fixed by removing that call from
   `dispose()` and adding `mounted` guards to `_appendLog()`, the async continuation in
   `_initBridge()`, and `_handleCubeClick()`.
3. **Dev-server stale compilation.** After fixing (2), the running `flutter run -d web-server`
   process kept serving the old compiled output — confirmed because the error stack trace still
   referenced pre-fix line numbers even after the source file was verified correct on disk.
   Fixed by fully stopping and restarting the dev server to force a genuine recompile. Noted as
   a tooling behavior to watch for, not an application bug.
4. **CanvasKit + Google Fonts CDN fetch in the `--release` build — real, unresolved, and not
   caused by Three.js.** Flutter's default web bootstrap (`flutter_bootstrap.js`'s
   `_flutter.buildConfig`) fetches `canvaskit.wasm`/`canvaskit.js` from
   `https://www.gstatic.com/flutter-canvaskit/...` unless `config.useLocalCanvasKit` or
   `config.canvasKitBaseUrl` is explicitly set, and separately fetches a Roboto `.woff2` from
   `fonts.gstatic.com`. Both were observed via
   `performance.getEntriesByType('resource')` against the served `--release` build. This is a
   **Flutter platform default that applies to the whole app, not specific to this spike or to
   Three.js** — the vendored Three.js files themselves load with zero external requests, exactly
   as required. The documented fix (per Flutter's own web-initialization docs, confirmed via
   `curl`) is a custom `web/flutter_bootstrap.js` template calling
   `_flutter.loader.load({config: {canvasKitBaseUrl: "/canvaskit/..."}})`. That file lives at
   the project root and is shared by every Flutter web build, including the real shipped app —
   changing it was explicitly out of scope for an isolated, deletable spike per the Gate 6 GO
   instructions ("Ne touche pas aux fonctionnalités déjà livrées"). **Left unresolved by
   design**, flagged here, and carried into the Gate 7 proposal below as a prerequisite.
5. **Browser-automation tooling artifacts, not application bugs.** The automation browser pane's
   `screenshot` action intermittently failed ("not displayed, so the page is not compositing
   frames"), worked around via direct DOM/JS inspection; `read_console_messages` appeared to
   return a stale buffer across navigations within the same tab, worked around by testing in a
   fresh tab. Both resolved on their own and were confirmed as tooling limitations, not app
   behavior, through independent evidence (decisive re-tests, fresh tabs, DOM-level checks).

## 4. Technical choice justified

- **No Three.js wrapper/Dart package was added.** `dart:js_interop` has been stable since Dart
  3.3; this project runs Dart 3.12.2 / Flutter 3.44.8. It supports calling plain JS global
  functions and properties directly, including automatic `int`/`double`/`String`/`bool`
  conversion, which is all the Flutter → Three.js command surface needed
  (`iNovaSpike3D.init/setRotationSpeed/setOnCubeClick/getFps/dispose`). No Flutter/Three.js
  interop package on pub.dev was needed for this — see
  [`three_bridge_interop.dart`](../../frontend/lib/spike_3d/three_bridge_interop.dart).
- **`package:web` (`^1.1.0`) is the one added pub dependency**, and it is not Three.js-specific:
  it is the Dart team's own typed successor to `dart:html`, used only to create the container
  `<div>` and register it with `dart:ui_web`'s `platformViewRegistry` (`HtmlElementView`'s
  standard mechanism for embedding a raw DOM element that a JS library then takes over).
- **Three.js itself is vendored, not installed via any Dart package system**, because it's a
  JavaScript library with no pub.dev equivalent — vendoring the built JS file and serving it as
  a static asset is the standard way to consume a JS library from Flutter web. Provenance
  (official npm registry tarball, `three@0.180.0`, MIT license) is documented in
  [`PROVENANCE.md`](../../frontend/web/spike3d/vendor/three/PROVENANCE.md).

## 5. Verdict

### READY — for the question this spike was built to answer

Flutter Web can host and drive a Three.js/WebGL scene with reliable, real, bidirectional
communication, using native `dart:js_interop` plus one small typed-DOM dependency
(`package:web`), with the 3D engine itself fully vendored and requiring zero external network
access — proven against both the dev server and a served `--release` build, across multiple
navigate-away/navigate-back and reload cycles, with no console errors and no shipped feature
touched.

### One mandatory, honestly-flagged prerequisite — not a Three.js problem

The `--release` build currently fetches CanvasKit and a Roboto font from `gstatic.com` by
Flutter's own default, unrelated to this spike's architecture. This does not fail the spike's
core question, but it does mean the **whole app**, as configured today, is not yet fully
CDN-free in production. This must be fixed — via a shared `web/flutter_bootstrap.js` override —
before or as the first step of Gate 7, since it affects the real app's release build too, not
just the 3D layer. It was not fixed inside Gate 6 because doing so requires editing a
project-root file shared with the already-shipped app, which the Gate 6 isolation mandate
explicitly excluded.

No ADR was created for 3D architecture in Gate 6, per the explicit instruction that the
definitive architectural choice should wait until after measurement and before real 3D World
work begins. [ADR-0002](../adr/0002-threejs-3d-world.md) (Three.js/WebGL, already Accepted)
stands as-is; this spike is evidence in support of it, not a new decision.

## 6. Gate 7 proposal (proposal only — no implementation, no commit)

If GO is given, Gate 7 would be the **first real 3D World increment**, scoped as follows:

1. **Prerequisite, step zero:** add `web/flutter_bootstrap.js` with `canvasKitBaseUrl` pointed at
   a locally-vendored CanvasKit (and the Roboto font handled the same way, or an explicit
   accepted-Google-Fonts-dependency decision presented to you first if a local font isn't
   preferred) — this is a shared, whole-app file, so it needs its own explicit sign-off before
   touching it, since it's the first Gate 7 change that isn't isolated to a spike directory.
2. **A single, minimal real scene** wired into the actual app (`main.dart`/`app_router.dart`),
   not the spike's standalone entrypoint — reusing the same `dart:js_interop` +
   `HtmlElementView` + vendored-Three.js pattern validated here, but replacing the spike's cube
   with the first real primitive from the target scene per
   [`04-3d-world/architecture.md`](../04-3d-world/architecture.md) (still no GLTF/avatar/Aira —
   those stay blocked/PLANNED).
3. **One real bridge event with real consequences**, per the contract already documented in
   [`04-3d-world/2d-3d-integration.md`](../04-3d-world/2d-3d-integration.md): a 3D object click
   triggers an actual Flutter navigation to an existing 2D screen (e.g., News or Missions) —
   proving the "3D interaction must also work identically from 2D UI" rule from that document by
   construction, since the target screen already has a normal 2D entry point.
2D/3D integration protocol would move from `[PLANNED]` to a documented, versioned contract at
that point — which is itself a small architecturally-significant decision to present to you
before writing it, not something to decide silently mid-implementation.

Explicitly out of scope for Gate 7 unless separately authorized: real map/level content, GLTF
pipeline, avatar, Aira/Rive integration (still blocked on the `.riv` asset), camera system beyond
the minimum needed to view one scene, any Phase 4+/5/6 module.

## Related documentation

- [GATE 6 GO instructions — see conversation record; constraints reproduced above]
- [`three.js/ADR-0002`](../adr/0002-threejs-3d-world.md)
- [2D/3D Integration](../04-3d-world/2d-3d-integration.md)
- [3D World Architecture](../04-3d-world/architecture.md)
- [Three.js](../04-3d-world/threejs.md)
- [PROJECT_STATUS.md](../PROJECT_STATUS.md)
