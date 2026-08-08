class NewsItem {
  const NewsItem({
    required this.id,
    required this.title,
    required this.link,
    required this.sourceName,
    this.excerpt,
    this.publishedAt,
  });

  final String id;
  final String title;
  final String link;
  final String sourceName;
  final String? excerpt;
  final DateTime? publishedAt;

  factory NewsItem.fromJson(Map<String, dynamic> json) => NewsItem(
        id: json['id'] as String,
        title: json['title'] as String,
        link: json['link'] as String,
        sourceName: json['source_name'] as String,
        excerpt: json['excerpt'] as String?,
        publishedAt: json['published_at'] == null ? null : DateTime.parse(json['published_at'] as String),
      );
}
