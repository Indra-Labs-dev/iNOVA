// Gate 7 — conditional export: real Three.js-backed WorldScreen on web,
// a plain placeholder everywhere else. dart.library.js_interop is only
// declared available on web compile targets (dart2js/dart2wasm/ddc), never
// on the Dart VM — this is the standard Flutter pattern for web-only UI
// that must still compile for non-web targets (native builds, and
// `flutter test`'s default VM-based test runner). See world_screen_web.dart
// and world_screen_stub.dart for the two implementations.
export 'world_screen_stub.dart' if (dart.library.js_interop) 'world_screen_web.dart';
