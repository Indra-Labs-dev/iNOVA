import '../data/news_item.dart';

enum NewsScreenStatus { idle, loading, refreshing, success, error }

class NewsState {
  const NewsState({
    this.status = NewsScreenStatus.idle,
    this.items = const [],
    this.errorMessage,
  });

  final NewsScreenStatus status;
  final List<NewsItem> items;
  final String? errorMessage;

  NewsState copyWith({
    NewsScreenStatus? status,
    List<NewsItem>? items,
    String? errorMessage,
  }) {
    return NewsState(
      status: status ?? this.status,
      items: items ?? this.items,
      errorMessage: errorMessage,
    );
  }
}
