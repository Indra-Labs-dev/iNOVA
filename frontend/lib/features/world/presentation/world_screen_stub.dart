// Gate 7 — non-web fallback for WorldScreen, selected by the conditional
// export in world_screen.dart. The real implementation (world_screen_web.dart)
// needs dart:js_interop/dart:ui_web/package:web, none of which exist outside
// a web compile target — this stub exists purely so app_router.dart (and
// anything that imports it, including every test) still compiles for
// non-web targets like `flutter test`'s default Dart VM runner. The route
// is only ever reachable in the shipped app, which is web-only today.
import 'package:flutter/material.dart';

class WorldScreen extends StatelessWidget {
  const WorldScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('iNOVA World (preview)')),
      body: const Center(child: Text('The 3D World is only available in the web build.')),
    );
  }
}
