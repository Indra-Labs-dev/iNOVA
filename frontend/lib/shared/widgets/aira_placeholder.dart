// Static placeholder for Aira — see docs/05-mascot/overview.md and
// docs/adr/0009-mascot-naming-aira.md. Deliberately NOT a Rive integration
// yet (Phase 2, see docs/16-roadmap/phases.md); this only proves the shell
// has a slot for the mascot.
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
        Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: const LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [INovaColors.cyan, INovaColors.purple],
            ),
          ),
          child: Icon(
            Icons.auto_awesome,
            color: INovaColors.white,
            size: size * 0.45,
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
