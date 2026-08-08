// Riverpod controller tests — no real HTTP, per
// docs/14-testing/frontend-tests.md.
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:inova_frontend/core/auth/auth_session.dart';
import 'package:inova_frontend/core/networking/api_exception.dart';
import 'package:inova_frontend/features/missions/application/mission_controller.dart';
import 'package:inova_frontend/features/missions/application/mission_state.dart';
import 'package:inova_frontend/features/missions/data/mission_repository.dart';
import 'package:inova_frontend/features/missions/data/mission_result.dart';

class _FakeMissionRepository implements MissionRepository {
  _FakeMissionRepository(this._call);

  final Future<MissionResult> Function(String goal, String token) _call;

  @override
  Future<MissionResult> start(String goal, {required String accessToken}) =>
      _call(goal, accessToken);
}

void main() {
  test('start() fails fast with a clear error when not signed in', () async {
    final container = ProviderContainer(
      overrides: [
        missionRepositoryProvider.overrideWithValue(
          _FakeMissionRepository((g, t) async => throw StateError('should not be called')),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(missionControllerProvider.notifier).start('anything');

    final state = container.read(missionControllerProvider);
    expect(state.status, MissionScreenStatus.error);
    expect(state.errorMessage, 'Sign in first.');
  });

  test('start() transitions idle -> loading -> success and passes the token through', () async {
    String? capturedToken;
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        missionRepositoryProvider.overrideWithValue(
          _FakeMissionRepository((goal, token) async {
            capturedToken = token;
            return const MissionResult(
              status: 'completed',
              answer: 'Python 3.14 was released.',
              xpAwarded: 10,
            );
          }),
        ),
      ],
    );
    addTearDown(container.dispose);

    expect(container.read(missionControllerProvider).status, MissionScreenStatus.idle);

    await container.read(missionControllerProvider.notifier).start('What is new?');

    final state = container.read(missionControllerProvider);
    expect(state.status, MissionScreenStatus.success);
    expect(state.result!.isCompleted, isTrue);
    expect(state.result!.xpAwarded, 10);
    expect(capturedToken, 'fake-token');
  });

  test('start() surfaces the server-reported failure without inventing an XP value', () async {
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        missionRepositoryProvider.overrideWithValue(
          _FakeMissionRepository(
            (goal, token) async => const MissionResult(
              status: 'failed',
              answer: '',
              xpAwarded: 0,
              failureReason: 'permission_denied',
            ),
          ),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(missionControllerProvider.notifier).start('anything');

    final state = container.read(missionControllerProvider);
    expect(state.status, MissionScreenStatus.success);
    expect(state.result!.isCompleted, isFalse);
    expect(state.result!.xpAwarded, 0);
    expect(state.result!.failureReason, 'permission_denied');
  });

  test('start() surfaces ApiException message on failure', () async {
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        missionRepositoryProvider.overrideWithValue(
          _FakeMissionRepository(
            (g, t) async => throw const ApiException(
              statusCode: 401,
              code: 'invalid_token',
              message: 'Invalid or expired access token.',
            ),
          ),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(missionControllerProvider.notifier).start('anything');

    final state = container.read(missionControllerProvider);
    expect(state.status, MissionScreenStatus.error);
    expect(state.errorMessage, 'Invalid or expired access token.');
  });
}

class _SignedInSession extends AuthSessionController {
  @override
  AuthSession build() => const AuthSession(accessToken: 'fake-token', email: 'test@inova.dev');
}
