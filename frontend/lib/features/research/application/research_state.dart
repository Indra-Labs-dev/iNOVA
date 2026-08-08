import '../data/research_result.dart';

enum ResearchStatus { idle, loading, success, error }

class ResearchState {
  const ResearchState({
    this.status = ResearchStatus.idle,
    this.result,
    this.errorMessage,
  });

  final ResearchStatus status;
  final ResearchResult? result;
  final String? errorMessage;

  ResearchState copyWith({ResearchStatus? status, ResearchResult? result, String? errorMessage}) {
    return ResearchState(
      status: status ?? this.status,
      result: result ?? this.result,
      errorMessage: errorMessage,
    );
  }
}
