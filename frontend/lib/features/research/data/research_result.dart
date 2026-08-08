import 'research_source.dart';

class ResearchResult {
  const ResearchResult({
    required this.answer,
    required this.sources,
    required this.outcome,
  });

  final String answer;
  final List<ResearchSource> sources;
  final String outcome;

  factory ResearchResult.fromJson(Map<String, dynamic> json) => ResearchResult(
        answer: json['answer'] as String? ?? '',
        sources: (json['sources'] as List<dynamic>? ?? [])
            .map((s) => ResearchSource.fromJson(s as Map<String, dynamic>))
            .toList(),
        outcome: json['outcome'] as String? ?? '',
      );
}
