// Gate 6 spike — native dart:js_interop bindings to web/spike3d/three_bridge.js.
// No third-party Dart package for the Three.js side of this bridge: modern
// dart:js_interop (stable since Dart 3.3; this project is on Dart 3.12)
// supports calling plain JS global functions/properties directly, including
// automatic conversion for int/double/String/bool — no wrapper package
// needed for that half of the bridge. The only added package is
// package:web, used solely for DOM element creation/platform-view
// registration (see spike_3d_screen.dart), not for anything Three.js-specific.
import 'dart:js_interop';

@JS('iNovaSpike3D.init')
external void jsInit(String containerId);

@JS('iNovaSpike3D.setRotationSpeed')
external void jsSetRotationSpeed(double value);

@JS('iNovaSpike3D.setOnCubeClick')
external void jsSetOnCubeClick(JSFunction callback);

@JS('iNovaSpike3D.getFps')
external int jsGetFps();

@JS('iNovaSpike3D.dispose')
external void jsDispose();

/// True once web/spike3d/three_bridge.js has finished loading as an ES
/// module and installed `window.iNovaSpike3D`. Checked via plain property
/// lookup on the global object — no assumption that the script has loaded
/// just because we requested it.
@JS('iNovaSpike3D')
external JSAny? get iNovaSpike3DGlobal;
