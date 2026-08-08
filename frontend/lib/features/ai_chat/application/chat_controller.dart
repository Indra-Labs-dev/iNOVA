import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_session.dart';
import '../../../core/networking/api_exception.dart';
import '../data/ai_chat_repository.dart';
import 'chat_state.dart';

class ChatController extends Notifier<ChatState> {
  @override
  ChatState build() => const ChatState();

  /// Reuses the most recent conversation if one already exists for this
  /// user (so a re-login after a reload finds the same history — see
  /// docs/06-ai/memory.md), otherwise starts a new one.
  Future<void> initialize() async {
    final session = ref.read(authSessionProvider);
    if (!session.isAuthenticated) {
      state = const ChatState(status: ChatStatus.error, errorMessage: 'Sign in first.');
      return;
    }

    state = state.copyWith(status: ChatStatus.loading);
    try {
      final repository = ref.read(aiChatRepositoryProvider);
      final conversations = await repository.listConversations(accessToken: session.accessToken!);
      final conversation = conversations.isNotEmpty
          ? conversations.first
          : await repository.createConversation(accessToken: session.accessToken!);

      final messages = await repository.listMessages(conversation.id, accessToken: session.accessToken!);
      state = ChatState(status: ChatStatus.idle, conversationId: conversation.id, messages: messages);
    } on ApiException catch (exception) {
      state = ChatState(status: ChatStatus.error, errorMessage: exception.message);
    } catch (_) {
      state = const ChatState(
        status: ChatStatus.error,
        errorMessage: 'Something went wrong. Is the backend running?',
      );
    }
  }

  Future<void> sendMessage(String content) async {
    final session = ref.read(authSessionProvider);
    final conversationId = state.conversationId;
    if (!session.isAuthenticated || conversationId == null) {
      state = state.copyWith(status: ChatStatus.error, errorMessage: 'Sign in first.');
      return;
    }

    state = state.copyWith(status: ChatStatus.thinking);
    try {
      final (userMessage, assistantMessage) = await ref
          .read(aiChatRepositoryProvider)
          .sendMessage(conversationId, content, accessToken: session.accessToken!);
      state = state.copyWith(
        status: ChatStatus.success,
        messages: [...state.messages, userMessage, assistantMessage],
      );
    } on ApiException catch (exception) {
      state = state.copyWith(status: ChatStatus.error, errorMessage: exception.message);
    } catch (_) {
      state = state.copyWith(
        status: ChatStatus.error,
        errorMessage: 'Something went wrong. Is the backend running?',
      );
    }
  }
}

final chatControllerProvider = NotifierProvider<ChatController, ChatState>(
  ChatController.new,
);
