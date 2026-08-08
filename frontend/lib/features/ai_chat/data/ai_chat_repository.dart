// Repository for the AI Companion chat — see docs/06-ai/memory.md (Gate 4:
// short-term conversation memory only). Talks to /api/v1/conversations,
// which is authenticated — unlike Phase 0's /ai/chat, this persists
// history server-side (see docs/09-backend/api-design.md deprecation note
// on /ai/chat).
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/networking/api_client.dart';
import 'chat_message.dart';
import 'conversation.dart';

class AiChatRepository {
  AiChatRepository(this._client);

  final ApiClient _client;

  Future<List<Conversation>> listConversations({required String accessToken}) async {
    final response = await _client.getJson('/conversations', authToken: accessToken);
    return (response as List<dynamic>)
        .map((c) => Conversation.fromJson(c as Map<String, dynamic>))
        .toList();
  }

  Future<Conversation> createConversation({required String accessToken}) async {
    final response = await _client.postJson('/conversations', body: {}, authToken: accessToken);
    return Conversation.fromJson(response);
  }

  Future<List<ChatMessage>> listMessages(String conversationId, {required String accessToken}) async {
    final response = await _client.getJson('/conversations/$conversationId/messages', authToken: accessToken);
    return (response as List<dynamic>)
        .map((m) => ChatMessage.fromJson(m as Map<String, dynamic>))
        .toList();
  }

  Future<(ChatMessage, ChatMessage)> sendMessage(
    String conversationId,
    String content, {
    required String accessToken,
  }) async {
    final response = await _client.postJson(
      '/conversations/$conversationId/messages',
      body: {'content': content},
      authToken: accessToken,
    );
    final userMessage = ChatMessage.fromJson(response['user_message'] as Map<String, dynamic>);
    final assistantMessage = ChatMessage.fromJson(response['assistant_message'] as Map<String, dynamic>);
    return (userMessage, assistantMessage);
  }
}

final aiChatRepositoryProvider = Provider<AiChatRepository>(
  (ref) => AiChatRepository(ref.watch(apiClientProvider)),
);
