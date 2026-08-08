class ResearchSource {
  const ResearchSource({required this.title, required this.link});

  final String title;
  final String link;

  factory ResearchSource.fromJson(Map<String, dynamic> json) => ResearchSource(
        title: json['title'] as String? ?? '',
        link: json['link'] as String? ?? '',
      );
}
