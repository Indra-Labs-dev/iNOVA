import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_session.dart';
import '../../../core/networking/api_exception.dart';
import '../data/mission_repository.dart';
import 'mission_state.dart';

class MissionController extends Notifier<MissionState> {
  @override
  MissionState build() => const MissionState();

  Future<void> start(String goal) async {
    final session = ref.read(authSessionProvider);
    if (!session.isAuthenticated) {
      state = const MissionState(
        status: MissionScreenStatus.error,
        errorMessage: 'Sign in first.',
      );
      return;
    }

    state = state.copyWith(status: MissionScreenStatus.loading);
    try {
      final result = await ref
          .read(missionRepositoryProvider)
          .start(goal, accessToken: session.accessToken!);
      state = MissionState(status: MissionScreenStatus.success, result: result);
    } on ApiException catch (exception) {
      state = MissionState(status: MissionScreenStatus.error, errorMessage: exception.message);
    } catch (_) {
      state = const MissionState(
        status: MissionScreenStatus.error,
        errorMessage: 'Something went wrong. Is the backend running?',
      );
    }
  }
}

final missionControllerProvider = NotifierProvider<MissionController, MissionState>(
  MissionController.new,
);
