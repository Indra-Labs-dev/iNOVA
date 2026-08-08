// Minimal named-route table — see docs/03-frontend/navigation.md. Two
// routes; deliberately not go_router or similar to avoid a dependency this
// phase doesn't need yet (docs/15-development/dependency-policy.md).
import 'package:flutter/material.dart';

import '../../features/ai_chat/presentation/ai_chat_screen.dart';
import '../../features/research/presentation/research_screen.dart';

class AppRoutes {
  const AppRoutes._();

  static const String home = '/';
  static const String research = '/research';

  static Map<String, WidgetBuilder> get table => {
        home: (_) => const AiChatScreen(),
        research: (_) => const ResearchScreen(),
      };
}
