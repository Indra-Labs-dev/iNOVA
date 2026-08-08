// Status names deliberately mirror the mascot state vocabulary in
// docs/05-mascot/states.md (idle/thinking/success/error) so wiring Aira's
// real state machine later (Phase 2) is a matter of listening to this state,
// not redesigning it.
enum ChatStatus { idle, thinking, success, error }

class ChatState {
  const ChatState({
    this.status = ChatStatus.idle,
    this.lastResponse,
    this.errorMessage,
  });

  final ChatStatus status;
  final String? lastResponse;
  final String? errorMessage;

  ChatState copyWith({
    ChatStatus? status,
    String? lastResponse,
    String? errorMessage,
  }) {
    return ChatState(
      status: status ?? this.status,
      lastResponse: lastResponse ?? this.lastResponse,
      errorMessage: errorMessage,
    );
  }
}
