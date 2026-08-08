// Repository for the AI Hub Phase 0 slice — see docs/06-ai/architecture.md.
// Talks to POST /api/v1/ai/chat only; no memory, no tools (see
// docs/16-roadmap/mvp.md).
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/networking/api_client.dart';

class AiChatRepository {
  AiChatRepository(this._client);

  final ApiClient _client;

  Future<String> sendMessage(String message) async {
    final response = await _client.postJson(
      '/ai/chat',
      body: {'message': message},
    );
    return response['response'] as String;
  }
}

final aiChatRepositoryProvider = Provider<AiChatRepository>(
  (ref) => AiChatRepository(ref.watch(apiClientProvider)),
);
