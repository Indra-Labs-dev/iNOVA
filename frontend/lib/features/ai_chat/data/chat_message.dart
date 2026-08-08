class ChatMessage {
  const ChatMessage({required this.id, required this.role, required this.content});

  final String id;
  final String role;
  final String content;

  bool get isUser => role == 'user';

  factory ChatMessage.fromJson(Map<String, dynamic> json) => ChatMessage(
        id: json['id'] as String,
        role: json['role'] as String,
        content: json['content'] as String,
      );
}
