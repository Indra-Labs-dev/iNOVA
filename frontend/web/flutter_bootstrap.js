// iNOVA — Gate 7 (2026-08-08): custom bootstrap to keep the app fully local
// in production, per the standing "no external CDN" requirement.
//
// Without this file, Flutter's default flutter_bootstrap.js fetches
// canvaskit.js/canvaskit.wasm from https://www.gstatic.com/flutter-canvaskit/...
// (see docs/16-roadmap/gate-6-3d-spike-report.md, finding #4). `flutter build web`
// already copies the CanvasKit build the SDK ships with into build/web/canvaskit/
// as a normal static asset — canvasKitBaseUrl below just tells the loader to use
// that local copy instead of downloading it again from Google's CDN.
//
// The fontFallbackBaseUrl CDN fetch (Roboto / glyph-fallback fonts) is a
// separate, still-open finding — see docs/PROJECT_STATUS.md "Known gaps".
{{flutter_js}}
{{flutter_build_config}}
_flutter.loader.load({
  config: {
    canvasKitBaseUrl: "canvaskit/",
  },
});
