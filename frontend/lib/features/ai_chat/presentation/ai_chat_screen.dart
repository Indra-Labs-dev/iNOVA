// Gate 4 UI — see docs/06-ai/memory.md: real multi-turn chat backed by
// server-persisted history (bounded window, short-term memory only — no
// cross-conversation memory yet). Deliberately still not a dashboard: one
// scrolling message list + an input row, no Rive/3D/state machine yet
// (docs/16-roadmap/phases.md Phase 2+).
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_session.dart';
import '../../../core/routing/app_router.dart';
import '../../../core/theme/inova_spacing.dart';
import '../../../shared/widgets/primary_button.dart';
import '../application/chat_controller.dart';
import '../application/chat_state.dart';
import '../data/chat_message.dart';

class AiChatScreen extends ConsumerWidget {
  const AiChatScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final session = ref.watch(authSessionProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('iNOVA — Aira'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pushNamed(context, AppRoutes.world),
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [Text('3D World'), SizedBox(width: 4), Icon(Icons.arrow_forward, size: 16)],
            ),
          ),
          TextButton(
            onPressed: () => Navigator.pushNamed(context, AppRoutes.research),
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [Text('ResearchAgent'), SizedBox(width: 4), Icon(Icons.arrow_forward, size: 16)],
            ),
          ),
        ],
      ),
      body: SafeArea(
        child: session.isAuthenticated ? const _ChatBody() : const _SignInGate(),
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
      if (mounted) {
        await ref.read(chatControllerProvider.notifier).initialize();
      }
    } catch (_) {
      setState(() => _error = 'Sign-in failed. Register via the API first if needed.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 420),
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(INovaSpacing.lg),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text('Sign in to talk to Aira.'),
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
          ),
        ),
      ),
    );
  }
}

class _ChatBody extends ConsumerStatefulWidget {
  const _ChatBody();

  @override
  ConsumerState<_ChatBody> createState() => _ChatBodyState();
}

class _ChatBodyState extends ConsumerState<_ChatBody> {
  final _input = TextEditingController();
  final _scrollController = ScrollController();
  bool _initialized = false;

  @override
  void initState() {
    super.initState();
    // A reload lands here with a fresh (unauthenticated) session, so this
    // only actually runs right after sign-in — see _SignInGateState._submit,
    // which also calls initialize() directly once login succeeds.
    WidgetsBinding.instance.addPostFrameCallback((_) => _maybeInitialize());
  }

  void _maybeInitialize() {
    if (_initialized) return;
    _initialized = true;
    ref.read(chatControllerProvider.notifier).initialize();
  }

  @override
  void dispose() {
    _input.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!_scrollController.hasClients) return;
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeOut,
      );
    });
  }

  Future<void> _send() async {
    final content = _input.text.trim();
    if (content.isEmpty) return;
    _input.clear();
    await ref.read(chatControllerProvider.notifier).sendMessage(content);
    _scrollToBottom();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(chatControllerProvider);
    ref.listen(chatControllerProvider, (previous, next) {
      if (next.messages.length != (previous?.messages.length ?? 0)) _scrollToBottom();
    });

    return Column(
      children: [
        Expanded(child: _MessageList(state: state, scrollController: _scrollController)),
        if (state.status == ChatStatus.error && state.messages.isEmpty)
          Padding(
            padding: const EdgeInsets.all(INovaSpacing.sm),
            child: Text(
              state.errorMessage ?? 'Something went wrong.',
              style: const TextStyle(color: Colors.redAccent),
            ),
          ),
        _InputRow(controller: _input, state: state, onSend: _send),
      ],
    );
  }
}

class _MessageList extends StatelessWidget {
  const _MessageList({required this.state, required this.scrollController});

  final ChatState state;
  final ScrollController scrollController;

  @override
  Widget build(BuildContext context) {
    if (state.status == ChatStatus.loading) {
      return const Center(child: Text('Loading your conversation...'));
    }
    if (state.messages.isEmpty) {
      return const Center(child: Text('Say hello to Aira.'));
    }

    return ListView.builder(
      controller: scrollController,
      padding: const EdgeInsets.all(INovaSpacing.md),
      itemCount: state.messages.length + (state.status == ChatStatus.thinking ? 1 : 0),
      itemBuilder: (context, index) {
        if (index >= state.messages.length) {
          return const _ThinkingBubble();
        }
        return _MessageBubble(message: state.messages[index]);
      },
    );
  }
}

class _MessageBubble extends StatelessWidget {
  const _MessageBubble({required this.message});

  final ChatMessage message;

  @override
  Widget build(BuildContext context) {
    final isUser = message.isUser;
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        key: isUser ? null : const Key('assistant-message'),
        constraints: const BoxConstraints(maxWidth: 420),
        margin: const EdgeInsets.symmetric(vertical: INovaSpacing.xs),
        padding: const EdgeInsets.symmetric(horizontal: INovaSpacing.md, vertical: INovaSpacing.sm),
        decoration: BoxDecoration(
          color: isUser ? Colors.blueAccent.withValues(alpha: 0.25) : Colors.white.withValues(alpha: 0.08),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(message.content),
      ),
    );
  }
}

class _ThinkingBubble extends StatelessWidget {
  const _ThinkingBubble();

  @override
  Widget build(BuildContext context) {
    return const Align(
      alignment: Alignment.centerLeft,
      child: Padding(
        padding: EdgeInsets.symmetric(vertical: INovaSpacing.xs),
        child: Text('Aira is thinking...', style: TextStyle(fontStyle: FontStyle.italic)),
      ),
    );
  }
}

class _InputRow extends StatelessWidget {
  const _InputRow({required this.controller, required this.state, required this.onSend});

  final TextEditingController controller;
  final ChatState state;
  final VoidCallback onSend;

  @override
  Widget build(BuildContext context) {
    final sending = state.status == ChatStatus.thinking;
    return Padding(
      padding: const EdgeInsets.all(INovaSpacing.md),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: controller,
              enabled: !sending,
              decoration: const InputDecoration(border: OutlineInputBorder(), hintText: 'Message Aira...'),
              onSubmitted: (_) => onSend(),
            ),
          ),
          const SizedBox(width: INovaSpacing.sm),
          PrimaryButton(label: 'Send', isLoading: sending, onPressed: onSend),
        ],
      ),
    );
  }
}
