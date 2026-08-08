// Status names deliberately mirror the mascot state vocabulary in
// docs/05-mascot/states.md (idle/thinking/success/error) so wiring Aira's
// real state machine later (Phase 2) is a matter of listening to this state,
// not redesigning it.
import '../data/chat_message.dart';

enum ChatStatus { idle, loading, thinking, success, error }

class ChatState {
  const ChatState({
    this.status = ChatStatus.idle,
    this.conversationId,
    this.messages = const [],
    this.errorMessage,
  });

  final ChatStatus status;
  final String? conversationId;
  final List<ChatMessage> messages;
  final String? errorMessage;

  ChatState copyWith({
    ChatStatus? status,
    String? conversationId,
    List<ChatMessage>? messages,
    String? errorMessage,
  }) {
    return ChatState(
      status: status ?? this.status,
      conversationId: conversationId ?? this.conversationId,
      messages: messages ?? this.messages,
      errorMessage: errorMessage,
    );
  }
}
