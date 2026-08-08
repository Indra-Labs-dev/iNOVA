class Conversation {
  const Conversation({required this.id, required this.updatedAt});

  final String id;
  final DateTime updatedAt;

  factory Conversation.fromJson(Map<String, dynamic> json) => Conversation(
        id: json['id'] as String,
        updatedAt: DateTime.parse(json['updated_at'] as String),
      );
}
