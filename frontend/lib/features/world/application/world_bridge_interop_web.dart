// Gate 7 — native dart:js_interop bindings to web/world/world_bridge.js.
// Same rationale as the Gate 6 spike's three_bridge_interop.dart: no
// third-party Dart/Three.js interop package, dart:js_interop (stable since
// Dart 3.3) is sufficient for this small, hand-written command/event
// surface — see docs/16-roadmap/gate-6-3d-spike-report.md "Technical
// choice justified".
import 'dart:js_interop';

/// Must match `bridgeVersion` in web/world/world_bridge.js — checked at
/// init time so a future shape mismatch between the two sides is a loud
/// warning, not a silent bug (docs/04-3d-world/2d-3d-integration.md "Rules").
const String kWorldBridgeVersion = '1.0.0';

@JS('iNovaWorld.init')
external void jsInit(String containerId);

@JS('iNovaWorld.setAccentColor')
external void jsSetAccentColor(int hex);

@JS('iNovaWorld.setOnObjectClick')
external void jsSetOnObjectClick(JSFunction callback);

@JS('iNovaWorld.dispose')
external void jsDispose();

@JS('iNovaWorld.bridgeVersion')
external String? get jsBridgeVersion;

/// True once web/world/world_bridge.js has finished loading as an ES module
/// and installed `window.iNovaWorld` — checked via plain property lookup,
/// never assumed just because the script tag was requested.
@JS('iNovaWorld')
external JSAny? get iNovaWorldGlobal;
