class MissionResult {
  const MissionResult({
    required this.status,
    required this.answer,
    required this.xpAwarded,
    this.failureReason,
  });

  final String status;
  final String answer;
  final int xpAwarded;
  final String? failureReason;

  bool get isCompleted => status == 'completed';

  factory MissionResult.fromJson(Map<String, dynamic> json) => MissionResult(
        status: json['status'] as String? ?? '',
        answer: json['answer'] as String? ?? '',
        xpAwarded: json['xp_awarded'] as int? ?? 0,
        failureReason: json['failure_reason'] as String?,
      );
}
