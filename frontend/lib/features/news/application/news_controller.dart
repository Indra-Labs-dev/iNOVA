import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_session.dart';
import '../../../core/networking/api_exception.dart';
import '../data/news_repository.dart';
import 'news_state.dart';

class NewsController extends Notifier<NewsState> {
  @override
  NewsState build() => const NewsState();

  Future<void> load() async {
    final session = ref.read(authSessionProvider);
    if (!session.isAuthenticated) {
      state = const NewsState(status: NewsScreenStatus.error, errorMessage: 'Sign in first.');
      return;
    }

    state = state.copyWith(status: NewsScreenStatus.loading);
    try {
      final items = await ref.read(newsRepositoryProvider).digest(accessToken: session.accessToken!);
      state = NewsState(status: NewsScreenStatus.success, items: items);
    } on ApiException catch (exception) {
      state = NewsState(status: NewsScreenStatus.error, errorMessage: exception.message);
    } catch (_) {
      state = const NewsState(
        status: NewsScreenStatus.error,
        errorMessage: 'Something went wrong. Is the backend running?',
      );
    }
  }

  Future<void> refresh() async {
    final session = ref.read(authSessionProvider);
    if (!session.isAuthenticated) {
      state = state.copyWith(status: NewsScreenStatus.error, errorMessage: 'Sign in first.');
      return;
    }

    state = state.copyWith(status: NewsScreenStatus.refreshing);
    try {
      final repository = ref.read(newsRepositoryProvider);
      await repository.refresh(accessToken: session.accessToken!);
      final items = await repository.digest(accessToken: session.accessToken!);
      state = state.copyWith(status: NewsScreenStatus.success, items: items);
    } on ApiException catch (exception) {
      state = state.copyWith(status: NewsScreenStatus.error, errorMessage: exception.message);
    } catch (_) {
      state = state.copyWith(
        status: NewsScreenStatus.error,
        errorMessage: 'Something went wrong. Is the backend running?',
      );
    }
  }
}

final newsControllerProvider = NotifierProvider<NewsController, NewsState>(
  NewsController.new,
);
