import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_session.dart';
import '../../../core/networking/api_exception.dart';
import '../data/research_repository.dart';
import 'research_state.dart';

class ResearchController extends Notifier<ResearchState> {
  @override
  ResearchState build() => const ResearchState();

  Future<void> ask(String query) async {
    final session = ref.read(authSessionProvider);
    if (!session.isAuthenticated) {
      state = const ResearchState(
        status: ResearchStatus.error,
        errorMessage: 'Sign in first.',
      );
      return;
    }

    state = state.copyWith(status: ResearchStatus.loading);
    try {
      final result = await ref
          .read(researchRepositoryProvider)
          .research(query, accessToken: session.accessToken!);
      state = ResearchState(status: ResearchStatus.success, result: result);
    } on ApiException catch (exception) {
      state = ResearchState(status: ResearchStatus.error, errorMessage: exception.message);
    } catch (_) {
      state = const ResearchState(
        status: ResearchStatus.error,
        errorMessage: 'Something went wrong. Is the backend running?',
      );
    }
  }
}

final researchControllerProvider = NotifierProvider<ResearchController, ResearchState>(
  ResearchController.new,
);
