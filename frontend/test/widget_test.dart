// App boot + routing smoke test — see docs/14-testing/frontend-tests.md.
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:inova_frontend/main.dart';

void main() {
  testWidgets('app boots and shows the Phase 0 chat shell', (tester) async {
    await tester.pumpWidget(const ProviderScope(child: INovaApp()));

    expect(find.text('iNOVA'), findsOneWidget);
    expect(find.text('Intelligent Digital Universe'), findsOneWidget);
    expect(find.text('Start Conversation'), findsOneWidget);
    expect(find.text('Aira'), findsOneWidget);
  });
}
