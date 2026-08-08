// Riverpod controller test — no real HTTP call, per
// docs/14-testing/frontend-tests.md / docs/14-testing/agent-tests.md
// ("don't depend on a heavy backend when a fake suffices").
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:inova_frontend/core/networking/api_exception.dart';
import 'package:inova_frontend/features/ai_chat/application/chat_controller.dart';
import 'package:inova_frontend/features/ai_chat/application/chat_state.dart';
import 'package:inova_frontend/features/ai_chat/data/ai_chat_repository.dart';

class _FakeRepository implements AiChatRepository {
  _FakeRepository(this._response);

  final Future<String> Function() _response;

  @override
  Future<String> sendMessage(String message) => _response();
}

void main() {
  test('sendMessage transitions idle -> thinking -> success', () async {
    final container = ProviderContainer(
      overrides: [
        aiChatRepositoryProvider.overrideWithValue(
          _FakeRepository(() async => 'hello from Aira'),
        ),
      ],
    );
    addTearDown(container.dispose);

    expect(container.read(chatControllerProvider).status, ChatStatus.idle);

    final future = container.read(chatControllerProvider.notifier).sendMessage('hi');
    expect(container.read(chatControllerProvider).status, ChatStatus.thinking);

    await future;

    final state = container.read(chatControllerProvider);
    expect(state.status, ChatStatus.success);
    expect(state.lastResponse, 'hello from Aira');
  });

  test('sendMessage surfaces ApiException message on failure', () async {
    final container = ProviderContainer(
      overrides: [
        aiChatRepositoryProvider.overrideWithValue(
          _FakeRepository(
            () async => throw const ApiException(
              statusCode: 502,
              code: 'llm_unavailable',
              message: 'The local LLM is unavailable.',
            ),
          ),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(chatControllerProvider.notifier).sendMessage('hi');

    final state = container.read(chatControllerProvider);
    expect(state.status, ChatStatus.error);
    expect(state.errorMessage, 'The local LLM is unavailable.');
  });
}
