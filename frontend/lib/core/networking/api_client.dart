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
    return _decodeObject(response);
  }

  Future<dynamic> getJson(String path, {String? authToken}) async {
    final response = await _httpClient.get(
      Uri.parse('$_baseUrl$path'),
      headers: {if (authToken != null) 'Authorization': 'Bearer $authToken'},
    );
    return _decodeAny(response);
  }

  Map<String, dynamic> _decodeObject(http.Response response) {
    final decoded = _decodeAny(response);
    return decoded is Map<String, dynamic> ? decoded : <String, dynamic>{};
  }

  dynamic _decodeAny(http.Response response) {
    final decoded = response.body.isEmpty ? null : jsonDecode(response.body);

    if (response.statusCode >= 200 && response.statusCode < 300) {
      return decoded ?? <String, dynamic>{};
    }

    final error = decoded is Map<String, dynamic> ? decoded['error'] as Map<String, dynamic>? : null;
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
