// Gate 7 — first real 3D World increment (not the Gate 6 spike). One
// clickable primitive, colored from Flutter's real theme (never hardcoded
// in JS, per docs/04-3d-world/architecture.md "Principle": the 3D layer
// visualizes state, it never owns it), whose click event is a real
// Flutter navigation to Missions — see docs/04-3d-world/2d-3d-integration.md.
//
// No map, no GLTF/avatar/Aira, no camera system, no event bus — still an
// early, intentionally minimal increment (Phase 3 in docs/16-roadmap/phases.md
// is the full 3D World).
//
// Web-only implementation file (dart:js_interop, dart:ui_web, package:web
// are all unavailable outside a web compile target) — selected by
// world_screen.dart's conditional export. See that file for why: `flutter
// test` compiles for the Dart VM by default, which does not have these
// libraries, and a plain unconditional import here would break every test
// that transitively imports app_router.dart (i.e. all of them).
import 'dart:async';
import 'dart:js_interop';
import 'dart:ui_web' as ui_web;

import 'package:flutter/material.dart';
import 'package:web/web.dart' as web;

import '../../../core/routing/app_router.dart';
import '../application/world_bridge_interop_web.dart';

const _viewType = 'inova-world-container';
const _containerId = 'inova-world-container';
const _bridgeScriptSrc = 'world/world_bridge.js';

bool _viewFactoryRegistered = false;
Future<void>? _bridgeScriptLoadFuture;

void _registerViewFactoryOnce() {
  if (_viewFactoryRegistered) return;
  _viewFactoryRegistered = true;
  ui_web.platformViewRegistry.registerViewFactory(_viewType, (int viewId) {
    final container = web.document.createElement('div') as web.HTMLDivElement;
    container.id = _containerId;
    container.style.width = '100%';
    container.style.height = '100%';
    return container;
  });
}

/// Loads web/world/world_bridge.js as an ES module exactly once per page
/// load — never assumed to already be present, always awaited for real
/// (same pattern proven in the Gate 6 spike).
Future<void> _ensureBridgeScriptLoaded() {
  return _bridgeScriptLoadFuture ??= () async {
    if (iNovaWorldGlobal != null) return; // already loaded by a prior screen instance
    final completer = Completer<void>();
    final script = web.document.createElement('script') as web.HTMLScriptElement;
    script.type = 'module';
    script.addEventListener('load', ((web.Event _) => completer.complete()).toJS);
    script.addEventListener(
      'error',
      ((web.Event _) => completer.completeError(StateError('Failed to load $_bridgeScriptSrc'))).toJS,
    );
    script.src = _bridgeScriptSrc;
    web.document.head!.appendChild(script);
    return completer.future;
  }();
}

class WorldScreen extends StatefulWidget {
  const WorldScreen({super.key});

  @override
  State<WorldScreen> createState() => _WorldScreenState();
}

class _WorldScreenState extends State<WorldScreen> {
  bool _ready = false;
  bool _failed = false;

  @override
  void initState() {
    super.initState();
    _registerViewFactoryOnce();
    _initBridge();
  }

  Future<void> _initBridge() async {
    try {
      await _ensureBridgeScriptLoaded();
    } catch (_) {
      if (mounted) setState(() => _failed = true);
      return;
    }

    if (jsBridgeVersion != kWorldBridgeVersion) {
      debugPrint(
        'World bridge version mismatch: Dart expects $kWorldBridgeVersion, '
        'JS reports $jsBridgeVersion — check world_bridge.js and '
        'world_bridge_interop.dart are in sync.',
      );
    }

    // The platform view's <div> is created asynchronously by the browser
    // engine — poll briefly rather than assuming a single post-frame
    // callback is enough (same measured behavior as the Gate 6 spike).
    var attempts = 0;
    while (web.document.getElementById(_containerId) == null && attempts < 50) {
      await Future.delayed(const Duration(milliseconds: 20));
      attempts++;
    }
    if (!mounted) return; // disposed while the container-poll loop was awaiting
    if (web.document.getElementById(_containerId) == null) {
      setState(() => _failed = true);
      return;
    }

    jsInit(_containerId);
    jsSetOnObjectClick(_handleObjectClick.toJS);
    if (mounted) {
      jsSetAccentColor(Theme.of(context).colorScheme.primary.toARGB32() & 0xFFFFFF);
      setState(() => _ready = true);
    }
  }

  void _handleObjectClick() {
    if (!mounted) return;
    // The 3D layer only reports "the object was clicked" — Flutter alone
    // decides what that means (here: go to Missions). Three.js never calls
    // Navigator itself.
    Navigator.pushNamed(context, AppRoutes.missions);
  }

  @override
  void dispose() {
    // No setState()/UI update here — the widget is already unmounting (see
    // docs/16-roadmap/gate-6-3d-spike-report.md problem #2 for why).
    jsDispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('iNOVA World (preview)')),
      body: Column(
        children: [
          Expanded(
            child: Container(
              color: Colors.black,
              child: Stack(
                children: [
                  if (!_failed) const HtmlElementView(viewType: _viewType),
                  if (_failed)
                    const Center(
                      child: Text('3D World failed to load.', style: TextStyle(color: Colors.redAccent)),
                    )
                  else if (!_ready)
                    const Center(child: CircularProgressIndicator()),
                ],
              ),
            ),
          ),
          const Padding(
            padding: EdgeInsets.all(12),
            child: Text(
              'Preview: one object, colored from the app theme. Click it to go to Missions.',
              style: TextStyle(fontSize: 12),
            ),
          ),
        ],
      ),
    );
  }
}
