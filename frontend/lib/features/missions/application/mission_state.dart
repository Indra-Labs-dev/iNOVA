import '../data/mission_result.dart';

enum MissionScreenStatus { idle, loading, success, error }

class MissionState {
  const MissionState({
    this.status = MissionScreenStatus.idle,
    this.result,
    this.errorMessage,
  });

  final MissionScreenStatus status;
  final MissionResult? result;
  final String? errorMessage;

  MissionState copyWith({
    MissionScreenStatus? status,
    MissionResult? result,
    String? errorMessage,
  }) {
    return MissionState(
      status: status ?? this.status,
      result: result ?? this.result,
      errorMessage: errorMessage,
    );
  }
}
