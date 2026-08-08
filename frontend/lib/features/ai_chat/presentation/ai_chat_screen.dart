// Phase 0 UI — see docs/16-roadmap/mvp.md item 16: prove the frontend is
// operational and can complete the Flutter -> FastAPI -> Ollama -> Flutter
// loop. Not the final visual language (docs/03-frontend/design-system.md).
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/routing/app_router.dart';
import '../../../core/theme/inova_spacing.dart';
import '../../../shared/widgets/aira_placeholder.dart';
import '../../../shared/widgets/primary_button.dart';
import '../application/chat_controller.dart';
import '../application/chat_state.dart';

class AiChatScreen extends ConsumerStatefulWidget {
  const AiChatScreen({super.key});

  @override
  ConsumerState<AiChatScreen> createState() => _AiChatScreenState();
}

class _AiChatScreenState extends ConsumerState<AiChatScreen> {
  final _controller = TextEditingController(text: 'Say hello from iNOVA Phase 0.');

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final chatState = ref.watch(chatControllerProvider);

    return Scaffold(
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 480),
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(INovaSpacing.lg),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Image.asset('assets/images/logo.png', height: 56),
                  const SizedBox(height: INovaSpacing.sm),
                  Text(
                    'iNOVA',
                    style: Theme.of(context).textTheme.headlineMedium,
                  ),
                  const SizedBox(height: INovaSpacing.xs),
                  Text(
                    'Intelligent Digital Universe',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                  const SizedBox(height: INovaSpacing.xl),
                  TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      hintText: 'Ask Aira something…',
                    ),
                  ),
                  const SizedBox(height: INovaSpacing.md),
                  PrimaryButton(
                    label: 'Start Conversation',
                    isLoading: chatState.status == ChatStatus.thinking,
                    onPressed: () {
                      final message = _controller.text.trim();
                      if (message.isNotEmpty) {
                        ref.read(chatControllerProvider.notifier).sendMessage(message);
                      }
                    },
                  ),
                  const SizedBox(height: INovaSpacing.xl),
                  const AiraPlaceholder(),
                  const SizedBox(height: INovaSpacing.md),
                  _ResponseArea(state: chatState),
                  const SizedBox(height: INovaSpacing.lg),
                  TextButton(
                    onPressed: () => Navigator.pushNamed(context, AppRoutes.research),
                    child: const Text('Try ResearchAgent →'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _ResponseArea extends StatelessWidget {
  const _ResponseArea({required this.state});

  final ChatState state;

  @override
  Widget build(BuildContext context) {
    switch (state.status) {
      case ChatStatus.idle:
        return const SizedBox.shrink();
      case ChatStatus.thinking:
        return const Text('Aira is thinking…');
      case ChatStatus.success:
        return Text(
          state.lastResponse ?? '',
          textAlign: TextAlign.center,
          key: const Key('chat-response'),
        );
      case ChatStatus.error:
        return Text(
          state.errorMessage ?? 'Something went wrong.',
          style: const TextStyle(color: Colors.redAccent),
          textAlign: TextAlign.center,
        );
    }
  }
}
