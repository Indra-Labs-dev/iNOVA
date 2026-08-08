// Foundation theme only — see docs/03-frontend/design-system.md. This is
// deliberately not the final "futuristic/glass" visual language; it exists
// to prove the theme plumbing works (docs/07-development... item 7: don't
// chase the spectacular final design yet).
import 'package:flutter/material.dart';

import 'inova_colors.dart';

class AppTheme {
  const AppTheme._();

  static ThemeData get dark {
    final colorScheme = ColorScheme.fromSeed(
      seedColor: INovaColors.electricBlue,
      brightness: Brightness.dark,
      primary: INovaColors.electricBlue,
      secondary: INovaColors.cyan,
      tertiary: INovaColors.purple,
      error: INovaColors.neonOrange,
      surface: INovaColors.deepSpace,
    );

    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorScheme: colorScheme,
      scaffoldBackgroundColor: INovaColors.deepSpace,
      textTheme: const TextTheme().apply(
        bodyColor: INovaColors.white,
        displayColor: INovaColors.white,
      ),
    );
  }
}
