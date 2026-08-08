// Thin HTTP wrapper — see docs/03-frontend/state-management.md: this is the
// only layer aware of HTTP details; repositories use it, widgets never call
// it directly.
import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;

import '../config/app_config.dart';
import 'api_exception.dart';

class ApiClient {
  ApiClient({http.Client? httpClient, String? baseUrl})
      : _httpClient = httpClient ?? http.Client(),
        _baseUrl = baseUrl ?? AppConfig.apiBaseUrl;

  final http.Client _httpClient;
  final String _baseUrl;

  Future<Map<String, dynamic>> postJson(
    String path, {
    required Map<String, dynamic> body,
    String? authToken,
  }) async {
    final response = await _httpClient.post(
      Uri.parse('$_baseUrl$path'),
      headers: {
        'Content-Type': 'application/json',
        if (authToken != null) 'Authorization': 'Bearer $authToken',
      },
      body: jsonEncode(body),
    );

    final decoded = response.body.isEmpty
        ? <String, dynamic>{}
        : jsonDecode(response.body) as Map<String, dynamic>;

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return decoded;
    }

    final error = decoded['error'] as Map<String, dynamic>?;
    throw ApiException(
      statusCode: response.statusCode,
      code: error?['code'] as String? ?? 'unknown_error',
      message: error?['message'] as String? ?? 'Request failed.',
    );
  }

  void close() => _httpClient.close();
}

/// Single canonical provider — shared across features so there's only one
/// HTTP client (and, if it grows connection pooling/interceptors later,
/// only one place that needs it).
final apiClientProvider = Provider<ApiClient>((ref) => ApiClient());
