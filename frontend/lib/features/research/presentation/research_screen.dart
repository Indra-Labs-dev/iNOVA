// Phase 1 Gate 2 UI — see docs/07-agents/agents/research-agent.md and
// docs/09-backend/api-design.md. Deliberately minimal: question -> request
// -> loading -> answer -> sources. Not a dashboard (see this Gate's
// "Ne transforme pas encore l'interface en dashboard complexe").
//
// Includes a small inline sign-in gate since there is no dedicated auth
// feature yet (docs/adr/0010 exists at the backend; the frontend has no
// persisted session/login screen — see docs/PROJECT_STATUS.md known gaps).
// This is intentionally scoped to this screen, not a new app-wide feature.
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_session.dart';
import '../../../core/theme/inova_spacing.dart';
import '../../../shared/widgets/primary_button.dart';
import '../application/research_controller.dart';
import '../application/research_state.dart';

class ResearchScreen extends ConsumerWidget {
  const ResearchScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final session = ref.watch(authSessionProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Research (Aira)')),
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 480),
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(INovaSpacing.lg),
              child: session.isAuthenticated ? const _ResearchForm() : const _SignInGate(),
            ),
          ),
        ),
      ),
    );
  }
}

class _SignInGate extends ConsumerStatefulWidget {
  const _SignInGate();

  @override
  ConsumerState<_SignInGate> createState() => _SignInGateState();
}

class _SignInGateState extends ConsumerState<_SignInGate> {
  final _email = TextEditingController();
  final _password = TextEditingController();
  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      await ref.read(authSessionProvider.notifier).login(_email.text.trim(), _password.text);
    } catch (_) {
      setState(() => _error = 'Sign-in failed. Register via the API first if needed.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        const Text('Sign in to ask ResearchAgent a question.'),
        const SizedBox(height: INovaSpacing.md),
        TextField(
          controller: _email,
          decoration: const InputDecoration(border: OutlineInputBorder(), hintText: 'Email'),
        ),
        const SizedBox(height: INovaSpacing.sm),
        TextField(
          controller: _password,
          obscureText: true,
          decoration: const InputDecoration(border: OutlineInputBorder(), hintText: 'Password'),
        ),
        const SizedBox(height: INovaSpacing.md),
        PrimaryButton(label: 'Sign in', isLoading: _loading, onPressed: _submit),
        if (_error != null) ...[
          const SizedBox(height: INovaSpacing.sm),
          Text(_error!, style: const TextStyle(color: Colors.redAccent)),
        ],
      ],
    );
  }
}

class _ResearchForm extends ConsumerStatefulWidget {
  const _ResearchForm();

  @override
  ConsumerState<_ResearchForm> createState() => _ResearchFormState();
}

class _ResearchFormState extends ConsumerState<_ResearchForm> {
  final _query = TextEditingController(text: 'Give me the latest from the python_blog feed.');

  @override
  void dispose() {
    _query.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(researchControllerProvider);

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        TextField(
          controller: _query,
          decoration: const InputDecoration(border: OutlineInputBorder(), hintText: 'Ask a research question…'),
        ),
        const SizedBox(height: INovaSpacing.md),
        PrimaryButton(
          label: 'Ask ResearchAgent',
          isLoading: state.status == ResearchStatus.loading,
          onPressed: () {
            final query = _query.text.trim();
            if (query.isNotEmpty) {
              ref.read(researchControllerProvider.notifier).ask(query);
            }
          },
        ),
        const SizedBox(height: INovaSpacing.lg),
        _ResultArea(state: state),
      ],
    );
  }
}

class _ResultArea extends StatelessWidget {
  const _ResultArea({required this.state});

  final ResearchState state;

  @override
  Widget build(BuildContext context) {
    switch (state.status) {
      case ResearchStatus.idle:
        return const SizedBox.shrink();
      case ResearchStatus.loading:
        return const Text('Aira is researching…');
      case ResearchStatus.error:
        return Text(
          state.errorMessage ?? 'Something went wrong.',
          style: const TextStyle(color: Colors.redAccent),
        );
      case ResearchStatus.success:
        final result = state.result!;
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(result.answer, key: const Key('research-answer')),
            if (result.sources.isNotEmpty) ...[
              const SizedBox(height: INovaSpacing.md),
              Text('Sources', style: Theme.of(context).textTheme.labelLarge),
              for (final source in result.sources)
                Padding(
                  padding: const EdgeInsets.only(top: INovaSpacing.xs),
                  child: Text('• ${source.title}', style: const TextStyle(fontSize: 13)),
                ),
            ],
          ],
        );
    }
  }
}
