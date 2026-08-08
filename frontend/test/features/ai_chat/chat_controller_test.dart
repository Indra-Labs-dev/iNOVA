// Riverpod controller test — no real HTTP call, per
// docs/14-testing/frontend-tests.md / docs/14-testing/agent-tests.md
// ("don't depend on a heavy backend when a fake suffices").
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:inova_frontend/core/auth/auth_session.dart';
import 'package:inova_frontend/core/networking/api_exception.dart';
import 'package:inova_frontend/features/ai_chat/application/chat_controller.dart';
import 'package:inova_frontend/features/ai_chat/application/chat_state.dart';
import 'package:inova_frontend/features/ai_chat/data/ai_chat_repository.dart';
import 'package:inova_frontend/features/ai_chat/data/chat_message.dart';
import 'package:inova_frontend/features/ai_chat/data/conversation.dart';

class _FakeRepository implements AiChatRepository {
  _FakeRepository({
    this._existingConversations = const [],
    this._existingMessages = const [],
    this._onSendMessage,
  });

  final List<Conversation> _existingConversations;
  final List<ChatMessage> _existingMessages;
  final Future<(ChatMessage, ChatMessage)> Function()? _onSendMessage;

  @override
  Future<List<Conversation>> listConversations({required String accessToken}) async =>
      _existingConversations;

  @override
  Future<Conversation> createConversation({required String accessToken}) async =>
      Conversation(id: 'new-conversation', updatedAt: DateTime.now());

  @override
  Future<List<ChatMessage>> listMessages(String conversationId, {required String accessToken}) async =>
      _existingMessages;

  @override
  Future<(ChatMessage, ChatMessage)> sendMessage(
    String conversationId,
    String content, {
    required String accessToken,
  }) =>
      _onSendMessage!();
}

class _SignedInSession extends AuthSessionController {
  @override
  AuthSession build() => const AuthSession(accessToken: 'fake-token', email: 'test@inova.dev');
}

void main() {
  test('initialize() creates a conversation when none exist yet', () async {
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        aiChatRepositoryProvider.overrideWithValue(_FakeRepository()),
      ],
    );
    addTearDown(container.dispose);

    await container.read(chatControllerProvider.notifier).initialize();

    final state = container.read(chatControllerProvider);
    expect(state.status, ChatStatus.idle);
    expect(state.conversationId, 'new-conversation');
    expect(state.messages, isEmpty);
  });

  test('initialize() reuses the most recent existing conversation and loads its history', () async {
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        aiChatRepositoryProvider.overrideWithValue(
          _FakeRepository(
            existingConversations: [Conversation(id: 'existing-conv', updatedAt: DateTime.now())],
            existingMessages: const [ChatMessage(id: 'm1', role: 'user', content: "I'm working on iNOVA.")],
          ),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(chatControllerProvider.notifier).initialize();

    final state = container.read(chatControllerProvider);
    expect(state.conversationId, 'existing-conv');
    expect(state.messages, hasLength(1));
    expect(state.messages.first.content, "I'm working on iNOVA.");
  });

  test('sendMessage transitions idle -> thinking -> success and appends both turns', () async {
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        aiChatRepositoryProvider.overrideWithValue(
          _FakeRepository(
            onSendMessage: () async => (
              const ChatMessage(id: 'u1', role: 'user', content: 'hi'),
              const ChatMessage(id: 'a1', role: 'assistant', content: 'hello from Aira'),
            ),
          ),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(chatControllerProvider.notifier).initialize();
    expect(container.read(chatControllerProvider).status, ChatStatus.idle);

    final future = container.read(chatControllerProvider.notifier).sendMessage('hi');
    expect(container.read(chatControllerProvider).status, ChatStatus.thinking);

    await future;

    final state = container.read(chatControllerProvider);
    expect(state.status, ChatStatus.success);
    expect(state.messages.map((m) => m.content), ['hi', 'hello from Aira']);
  });

  test('sendMessage surfaces ApiException message on failure', () async {
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        aiChatRepositoryProvider.overrideWithValue(
          _FakeRepository(
            onSendMessage: () async => throw const ApiException(
              statusCode: 502,
              code: 'llm_unavailable',
              message: 'The local LLM is unavailable.',
            ),
          ),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(chatControllerProvider.notifier).initialize();
    await container.read(chatControllerProvider.notifier).sendMessage('hi');

    final state = container.read(chatControllerProvider);
    expect(state.status, ChatStatus.error);
    expect(state.errorMessage, 'The local LLM is unavailable.');
  });

  test('sendMessage fails fast with a clear error when not signed in', () async {
    final container = ProviderContainer(
      overrides: [
        aiChatRepositoryProvider.overrideWithValue(
          _FakeRepository(onSendMessage: () async => throw StateError('should not be called')),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(chatControllerProvider.notifier).sendMessage('hi');

    final state = container.read(chatControllerProvider);
    expect(state.status, ChatStatus.error);
    expect(state.errorMessage, 'Sign in first.');
  });
}
