// Riverpod controller tests — no real HTTP, per
// docs/14-testing/frontend-tests.md.
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:inova_frontend/core/auth/auth_session.dart';
import 'package:inova_frontend/core/networking/api_exception.dart';
import 'package:inova_frontend/features/news/application/news_controller.dart';
import 'package:inova_frontend/features/news/application/news_state.dart';
import 'package:inova_frontend/features/news/data/news_item.dart';
import 'package:inova_frontend/features/news/data/news_repository.dart';

class _FakeNewsRepository implements NewsRepository {
  _FakeNewsRepository({this.digestItems = const [], this.onRefresh});

  final List<NewsItem> digestItems;
  final Future<int> Function()? onRefresh;

  @override
  Future<List<NewsItem>> digest({required String accessToken}) async => digestItems;

  @override
  Future<int> refresh({required String accessToken}) => onRefresh!();
}

class _SignedInSession extends AuthSessionController {
  @override
  AuthSession build() => const AuthSession(accessToken: 'fake-token', email: 'test@inova.dev');
}

void main() {
  test('load() fails fast with a clear error when not signed in', () async {
    final container = ProviderContainer(
      overrides: [newsRepositoryProvider.overrideWithValue(_FakeNewsRepository())],
    );
    addTearDown(container.dispose);

    await container.read(newsControllerProvider.notifier).load();

    final state = container.read(newsControllerProvider);
    expect(state.status, NewsScreenStatus.error);
    expect(state.errorMessage, 'Sign in first.');
  });

  test('load() populates items from the digest', () async {
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        newsRepositoryProvider.overrideWithValue(
          _FakeNewsRepository(
            digestItems: const [
              NewsItem(id: '1', title: 'Python 3.15 released', link: 'https://example.com/1', sourceName: 'Python Insider'),
            ],
          ),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(newsControllerProvider.notifier).load();

    final state = container.read(newsControllerProvider);
    expect(state.status, NewsScreenStatus.success);
    expect(state.items, hasLength(1));
    expect(state.items.first.title, 'Python 3.15 released');
  });

  test('refresh() triggers a refresh then reloads the digest', () async {
    var refreshCalled = false;
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        newsRepositoryProvider.overrideWithValue(
          _FakeNewsRepository(
            digestItems: const [
              NewsItem(id: '1', title: 'New item', link: 'https://example.com/1', sourceName: 'Python Insider'),
            ],
            onRefresh: () async {
              refreshCalled = true;
              return 1;
            },
          ),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(newsControllerProvider.notifier).refresh();

    expect(refreshCalled, isTrue);
    final state = container.read(newsControllerProvider);
    expect(state.status, NewsScreenStatus.success);
    expect(state.items, hasLength(1));
  });

  test('load() surfaces ApiException message on failure', () async {
    final container = ProviderContainer(
      overrides: [
        authSessionProvider.overrideWith(() => _SignedInSession()),
        newsRepositoryProvider.overrideWithValue(
          _ThrowingNewsRepository(),
        ),
      ],
    );
    addTearDown(container.dispose);

    await container.read(newsControllerProvider.notifier).load();

    final state = container.read(newsControllerProvider);
    expect(state.status, NewsScreenStatus.error);
    expect(state.errorMessage, 'Session expired.');
  });
}

class _ThrowingNewsRepository implements NewsRepository {
  @override
  Future<List<NewsItem>> digest({required String accessToken}) async {
    throw const ApiException(statusCode: 401, code: 'invalid_token', message: 'Session expired.');
  }

  @override
  Future<int> refresh({required String accessToken}) async => 0;
}
