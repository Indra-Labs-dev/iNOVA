// Repository for the News Intelligence digest — see
// docs/08-modules/news-intelligence.md. Extractive digest only: the
// backend never runs AI summarization (deferred, see
// docs/adr/0014-defer-ai-summarization.md), so every field here is the
// source's own RSS text, verbatim.
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/networking/api_client.dart';
import 'news_item.dart';

class NewsRepository {
  NewsRepository(this._client);

  final ApiClient _client;

  Future<List<NewsItem>> digest({required String accessToken}) async {
    final response = await _client.getJson('/news', authToken: accessToken);
    return (response as List<dynamic>).map((i) => NewsItem.fromJson(i as Map<String, dynamic>)).toList();
  }

  Future<int> refresh({required String accessToken}) async {
    final response = await _client.postJson('/news/refresh', body: {}, authToken: accessToken);
    return response['items_new_total'] as int;
  }
}

final newsRepositoryProvider = Provider<NewsRepository>(
  (ref) => NewsRepository(ref.watch(apiClientProvider)),
);
