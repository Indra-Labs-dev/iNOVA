// Gate 6 — standalone entrypoint for the 3D feasibility spike. Deliberately
// separate from lib/main.dart: zero modification to the shipped app (Chat,
// Research, Missions, News, Auth) or its router. Run with:
//   flutter run -d web-server -t lib/spike_3d_main.dart --web-port 5174
// Build with:
//   flutter build web -t lib/spike_3d_main.dart -o build/spike3d --release
//
// Entirely removable: delete this file, lib/spike_3d/, web/spike3d/, and
// the `web:` line in pubspec.yaml, and nothing else in the app changes.
import 'package:flutter/material.dart';

import 'spike_3d/spike_3d_screen.dart';

void main() {
  runApp(const Spike3DApp());
}

class Spike3DApp extends StatelessWidget {
  const Spike3DApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'iNOVA — Gate 6 3D Spike',
      theme: ThemeData.dark(useMaterial3: true),
      home: const _SpikeMenuScreen(),
    );
  }
}

/// A trivial "away" screen so navigating to the spike and back exercises
/// real widget dispose/recreate of the HtmlElementView, not just a single
/// long-lived instance.
class _SpikeMenuScreen extends StatelessWidget {
  const _SpikeMenuScreen();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Gate 6 spike — menu')),
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('This is not part of the iNOVA app.'),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () => Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const Spike3DScreen()),
              ),
              child: const Text('Open 3D spike'),
            ),
          ],
        ),
      ),
    );
  }
}
