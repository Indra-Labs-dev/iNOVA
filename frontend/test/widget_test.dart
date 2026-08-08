// App boot + routing smoke test — see docs/14-testing/frontend-tests.md.
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:inova_frontend/main.dart';

void main() {
  testWidgets('app boots and shows the sign-in gate for the chat screen', (tester) async {
    await tester.pumpWidget(const ProviderScope(child: INovaApp()));

    expect(find.text('iNOVA — Aira'), findsOneWidget);
    expect(find.text('Sign in to talk to Aira.'), findsOneWidget);
  });
}
