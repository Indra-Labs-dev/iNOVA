// Static placeholder for Aira — see docs/05-mascot/overview.md and
// docs/adr/0009-mascot-naming-aira.md. Uses the real concept art
// (assets/images/mascotte-aira.png) but is deliberately NOT a Rive
// integration yet (Phase 2, see docs/16-roadmap/phases.md) — no animation,
// no state machine, just the static image in a fixed "idle" presentation.
import 'package:flutter/material.dart';

import '../../core/theme/inova_colors.dart';

class AiraPlaceholder extends StatelessWidget {
  const AiraPlaceholder({super.key, this.size = 96});

  final double size;

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ClipOval(
          child: Image.asset(
            'assets/images/mascotte-aira.png',
            width: size,
            height: size,
            fit: BoxFit.cover,
          ),
        ),
        const SizedBox(height: 8),
        const Text(
          'Aira',
          style: TextStyle(color: INovaColors.white, fontWeight: FontWeight.w600),
        ),
        const Text(
          '(placeholder — Rive integration is Phase 2)',
          style: TextStyle(color: Colors.white54, fontSize: 11),
        ),
      ],
    );
  }
}
