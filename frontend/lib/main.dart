// iNOVA — Copyright (c) 2026 Archange Elie Yatte (AEY)
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/routing/app_router.dart';
import 'core/theme/app_theme.dart';

void main() {
  runApp(const ProviderScope(child: INovaApp()));
}

class INovaApp extends StatelessWidget {
  const INovaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'iNOVA',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.dark,
      darkTheme: AppTheme.dark,
      initialRoute: AppRoutes.home,
      routes: AppRoutes.table,
    );
  }
}
