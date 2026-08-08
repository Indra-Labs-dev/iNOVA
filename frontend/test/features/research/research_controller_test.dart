// Riverpod controller tests — no real HTTP, per
// docs/14-testing/frontend-tests.md.
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:inova_frontend/core/auth/auth_session.dart';
import 'package:inova_frontend/core/networking/api_exception.dart';
import 'package:inova_frontend/features/research/application/research_controller.dart';
import 'package:inova_frontend/features/research/application/research_state.dart';
import 'package:inova_frontend/features/research/data/research_repository.dart';
import 'package:inova_frontend/features/research/data/research_result.dart';
import 'package:inova_frontend/features/research/data/research_source.dart';

class _FakeResearchRepository implements ResearchRepository {
  _FakeResearchRepository(this._call);

  final Future<ResearchResult> Function(String query, String token) _call;

  @override
  Future<ResearchResult> research(String query, {required String accessToken}) =>
      _call(query, accessToken);
}

void main() {
  test('ask() fails fast with a clear error when not signed in', () async {
    final container = ProviderContainer(
      overrides: [
        researchRepositoryProvider.overrideWithValue(
          _FakeResearchRepository((q, t) async => throw StateError('should not be called')),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(researchControllerProvider.notifier).ask('anything');

    final state = container.read(researchControllerProvider);
    expect(state.status, ResearchStatus.error);
    expect(state.errorMessage, 'Sign in first.');
  });

  test('ask() transitions idle -> loading -> success and passes the token through', () async {
    String? capturedToken;
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        researchRepositoryProvider.overrideWithValue(
          _FakeResearchRepository((q, token) async {
            capturedToken = token;
            return const ResearchResult(
              answer: 'Python 3.14 was released.',
              sources: [ResearchSource(title: 'Python 3.14 released', link: 'https://blog.python.org/1')],
              outcome: 'success',
            );
          }),
        ),
      ],
    );
    addTearDown(container.dispose);

    expect(container.read(researchControllerProvider).status, ResearchStatus.idle);

    await container.read(researchControllerProvider.notifier).ask('What is new?');

    final state = container.read(researchControllerProvider);
    expect(state.status, ResearchStatus.success);
    expect(state.result!.answer, 'Python 3.14 was released.');
    expect(state.result!.sources, hasLength(1));
    expect(capturedToken, 'fake-token');
  });

  test('ask() surfaces ApiException message on failure', () async {
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        researchRepositoryProvider.overrideWithValue(
          _FakeResearchRepository(
            (q, t) async => throw const ApiException(
              statusCode: 401,
              code: 'invalid_token',
              message: 'Invalid or expired access token.',
            ),
          ),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(researchControllerProvider.notifier).ask('anything');

    final state = container.read(researchControllerProvider);
    expect(state.status, ResearchStatus.error);
    expect(state.errorMessage, 'Invalid or expired access token.');
  });
}

class _SignedInSession extends AuthSessionController {
  @override
  AuthSession build() => const AuthSession(accessToken: 'fake-token', email: 'test@inova.dev');
}
