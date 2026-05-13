import 'package:flutter/material.dart';

class AppTheme {
  static const Color primary = Color(0xFF2563EB);
  static const Color success = Color(0xFF16A34A);
  static const Color warning = Color(0xFFD97706);
  static const Color danger = Color(0xFFDC2626);
  static const Color surface = Color(0xFFF8FAFC);
  static const Color cardBg = Colors.white;

  static ThemeData get theme => ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: primary,
          background: surface,
        ),
        useMaterial3: true,
        scaffoldBackgroundColor: surface,
        cardTheme: const CardTheme(
          color: cardBg,
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.all(Radius.circular(16)),
          ),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: primary,
          foregroundColor: Colors.white,
          elevation: 0,
        ),
      );

  static Color alertColor(dynamic level) {
    switch (level.toString()) {
      case 'AlertLevel.attention':
        return warning;
      case 'AlertLevel.emergency':
        return danger;
      default:
        return success;
    }
  }
}
