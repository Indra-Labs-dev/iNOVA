// Gate 3 MVP UI — see docs/08-modules/mission-system.md. Deliberately
// minimal: goal -> request -> loading -> "Mission complete +X XP" (or
// failure message). No leaderboard/achievements/levels/streaks/badges —
// those are out of scope for this Gate (docs/08-modules/gamification.md).
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_session.dart';
import '../../../core/theme/inova_spacing.dart';
import '../../../shared/widgets/primary_button.dart';
import '../application/mission_controller.dart';
import '../application/mission_state.dart';

class MissionScreen extends ConsumerWidget {
  const MissionScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final session = ref.watch(authSessionProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Missions')),
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 480),
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(INovaSpacing.lg),
              child: session.isAuthenticated ? const _MissionForm() : const _SignInHint(),
            ),
          ),
        ),
      ),
    );
  }
}

class _SignInHint extends StatelessWidget {
  const _SignInHint();

  @override
  Widget build(BuildContext context) {
    return const Text('Sign in on the Research screen first, then come back here.');
  }
}

class _MissionForm extends ConsumerStatefulWidget {
  const _MissionForm();

  @override
  ConsumerState<_MissionForm> createState() => _MissionFormState();
}

class _MissionFormState extends ConsumerState<_MissionForm> {
  final _goal = TextEditingController(text: 'Give me the latest from the python_blog feed.');

  @override
  void dispose() {
    _goal.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(missionControllerProvider);

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        TextField(
          controller: _goal,
          decoration: const InputDecoration(border: OutlineInputBorder(), hintText: 'What is your goal?'),
        ),
        const SizedBox(height: INovaSpacing.md),
        PrimaryButton(
          label: 'Start Mission',
          isLoading: state.status == MissionScreenStatus.loading,
          onPressed: () {
            final goal = _goal.text.trim();
            if (goal.isNotEmpty) {
              ref.read(missionControllerProvider.notifier).start(goal);
            }
          },
        ),
        const SizedBox(height: INovaSpacing.lg),
        _MissionResultArea(state: state),
      ],
    );
  }
}

class _MissionResultArea extends StatelessWidget {
  const _MissionResultArea({required this.state});

  final MissionState state;

  @override
  Widget build(BuildContext context) {
    switch (state.status) {
      case MissionScreenStatus.idle:
        return const SizedBox.shrink();
      case MissionScreenStatus.loading:
        return const Text('Aira is working on it…');
      case MissionScreenStatus.error:
        return Text(
          state.errorMessage ?? 'Something went wrong.',
          style: const TextStyle(color: Colors.redAccent),
        );
      case MissionScreenStatus.success:
        final result = state.result!;
        // The XP value shown here always comes from the server response —
        // never hardcoded — since only the backend computes it (see
        // docs/08-modules/mission-system.md "XP server-side only").
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              result.isCompleted
                  ? 'Mission complete +${result.xpAwarded} XP'
                  : 'Mission failed (${result.failureReason ?? "unknown reason"})',
              key: const Key('mission-outcome'),
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: result.isCompleted ? Colors.greenAccent : Colors.redAccent,
                  ),
            ),
            if (result.answer.isNotEmpty) ...[
              const SizedBox(height: INovaSpacing.sm),
              Text(result.answer),
            ],
          ],
        );
    }
  }
}
