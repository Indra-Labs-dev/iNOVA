import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/networking/api_exception.dart';
import '../data/ai_chat_repository.dart';
import 'chat_state.dart';

class ChatController extends Notifier<ChatState> {
  @override
  ChatState build() => const ChatState();

  Future<void> sendMessage(String message) async {
    state = state.copyWith(status: ChatStatus.thinking);
    try {
      final response = await ref.read(aiChatRepositoryProvider).sendMessage(message);
      state = ChatState(status: ChatStatus.success, lastResponse: response);
    } on ApiException catch (exception) {
      state = ChatState(status: ChatStatus.error, errorMessage: exception.message);
    } catch (_) {
      state = const ChatState(
        status: ChatStatus.error,
        errorMessage: 'Something went wrong. Is the backend running?',
      );
    }
  }
}

final chatControllerProvider = NotifierProvider<ChatController, ChatState>(
  ChatController.new,
);
