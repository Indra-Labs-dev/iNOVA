// Gate 6 — 3D World Feasibility Spike. NOT the real 3D World: one rotating
// cube, one command (rotation speed), one event (cube click). Purpose is
// exclusively to measure whether Flutter web can host and drive a
// Three.js/WebGL scene with reliable bidirectional communication — see
// docs/16-roadmap/ Gate 6 report for the measurements and verdict.
//
// Architectural rule under test: Flutter owns all application state.
// Three.js only (a) receives commands and (b) reports raw events — it
// never makes a navigation or business decision itself. This screen is
// the "Flutter State" side of `Flutter State -> Bridge -> Three.js Scene`
// and `Three.js Event -> Bridge -> Flutter State`.
import 'dart:async';
import 'dart:js_interop';
import 'dart:ui_web' as ui_web;

import 'package:flutter/material.dart';
import 'package:web/web.dart' as web;

import 'three_bridge_interop.dart';

const _viewType = 'inova-spike3d-container';
const _containerId = 'inova-spike3d-container';
const _bridgeScriptSrc = 'spike3d/three_bridge.js';

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

/// Loads web/spike3d/three_bridge.js as an ES module exactly once per page
/// load — never assumed to already be present, always awaited for real.
Future<void> _ensureBridgeScriptLoaded() {
  return _bridgeScriptLoadFuture ??= () async {
    if (iNovaSpike3DGlobal != null) return; // already loaded by a prior screen instance
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

class Spike3DScreen extends StatefulWidget {
  const Spike3DScreen({super.key});

  @override
  State<Spike3DScreen> createState() => _Spike3DScreenState();
}

class _Spike3DScreenState extends State<Spike3DScreen> {
  final _log = <String>[];
  String? _lastClickEvent;
  double _rotationSpeed = 0.01;
  int _fps = 0;
  Timer? _fpsTimer;
  bool _ready = false;
  DateTime? _tScreenBuilt;
  DateTime? _tSceneReady;

  @override
  void initState() {
    super.initState();
    _tScreenBuilt = DateTime.now();
    _registerViewFactoryOnce();
    _initBridge();
  }

  void _appendLog(String message) {
    if (!mounted) return; // the widget may have been disposed mid-await
    final elapsed = _tScreenBuilt == null ? 0 : DateTime.now().difference(_tScreenBuilt!).inMilliseconds;
    setState(() => _log.add('+${elapsed}ms  $message'));
  }

  Future<void> _initBridge() async {
    _appendLog('screen initState');
    try {
      await _ensureBridgeScriptLoaded();
      _appendLog('three_bridge.js loaded (ES module)');
    } catch (e) {
      _appendLog('FAILED to load three_bridge.js: $e');
      return;
    }

    // The platform view's <div> is created asynchronously by the browser
    // engine — poll briefly rather than assuming a single post-frame
    // callback is enough (measured behavior, not assumed).
    var attempts = 0;
    while (web.document.getElementById(_containerId) == null && attempts < 50) {
      await Future.delayed(const Duration(milliseconds: 20));
      attempts++;
    }
    if (web.document.getElementById(_containerId) == null) {
      _appendLog('FAILED: container div never appeared after ${attempts * 20}ms');
      return;
    }
    _appendLog('container div found after ${attempts * 20}ms');

    if (!mounted) return; // disposed while the container-poll loop was awaiting

    jsInit(_containerId);
    _tSceneReady = DateTime.now();
    final totalMs = _tSceneReady!.difference(_tScreenBuilt!).inMilliseconds;
    _appendLog('iNovaSpike3D.init() called — scene initialized, total load ${totalMs}ms');

    jsSetOnCubeClick(_handleCubeClick.toJS);
    jsSetRotationSpeed(_rotationSpeed);

    _fpsTimer = Timer.periodic(const Duration(seconds: 1), (_) {
      if (!mounted) return;
      setState(() => _fps = jsGetFps());
    });

    if (mounted) setState(() => _ready = true);
  }

  void _handleCubeClick(JSNumber timestampMs) {
    if (!mounted) return;
    final now = TimeOfDay.now();
    setState(() {
      _lastClickEvent = 'Cube clicked at ${now.format(context)} (JS performance.now()=${timestampMs.toDartDouble.toStringAsFixed(1)}ms)';
    });
    _appendLog('received cube-click event from Three.js');
  }

  void _setSpeed(double value) {
    setState(() => _rotationSpeed = value);
    jsSetRotationSpeed(value);
  }

  @override
  void dispose() {
    // No setState()/UI update here — the widget is already unmounting.
    // (Found live: calling _appendLog(), which calls setState(), from
    // dispose() throws "_lifecycleState != _ElementLifecycle.defunct" —
    // a real bug this spike's own navigate-away test caught.)
    _fpsTimer?.cancel();
    jsDispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Gate 6 — 3D Spike (not the real 3D World)')),
      body: Row(
        children: [
          Expanded(
            flex: 3,
            child: Container(
              color: Colors.black,
              child: const HtmlElementView(viewType: _viewType),
            ),
          ),
          Expanded(
            flex: 2,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Status: ${_ready ? "ready" : "loading…"}', style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 8),
                  Text('FPS (reported by Three.js): $_fps'),
                  const SizedBox(height: 16),
                  Text('Rotation speed: ${_rotationSpeed.toStringAsFixed(3)}'),
                  Slider(
                    value: _rotationSpeed,
                    min: 0.0,
                    max: 0.2,
                    onChanged: _ready ? _setSpeed : null,
                  ),
                  const SizedBox(height: 16),
                  const Text('Flutter → Three.js: use the slider above.', style: TextStyle(fontSize: 12)),
                  const SizedBox(height: 8),
                  const Text('Three.js → Flutter: click the cube.', style: TextStyle(fontSize: 12)),
                  const SizedBox(height: 8),
                  Text(
                    _lastClickEvent ?? '(no click received yet)',
                    key: const Key('last-click-event'),
                    style: const TextStyle(color: Colors.greenAccent),
                  ),
                  const Divider(height: 32),
                  Text('Load timeline', style: Theme.of(context).textTheme.titleSmall),
                  const SizedBox(height: 8),
                  Expanded(
                    child: ListView(
                      children: _log.map((l) => Text(l, style: const TextStyle(fontSize: 11, fontFamily: 'monospace'))).toList(),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
