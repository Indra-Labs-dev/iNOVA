import 'dart:convert';

import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';
import 'package:inova_frontend/core/networking/api_client.dart';
import 'package:inova_frontend/core/networking/api_exception.dart';

void main() {
  test('postJson returns decoded body on 2xx', () async {
    final mockClient = MockClient((request) async {
      return http.Response(jsonEncode({'response': 'hi', 'model': 'test'}), 200);
    });
    final client = ApiClient(httpClient: mockClient, baseUrl: 'http://test');

    final result = await client.postJson('/ai/chat', body: {'message': 'hello'});

    expect(result['response'], 'hi');
  });

  test('postJson throws ApiException parsed from the error envelope', () async {
    final mockClient = MockClient((request) async {
      return http.Response(
        jsonEncode({
          'error': {'code': 'invalid_credentials', 'message': 'Invalid email or password.', 'details': null}
        }),
        401,
      );
    });
    final client = ApiClient(httpClient: mockClient, baseUrl: 'http://test');

    expect(
      () => client.postJson('/auth/login', body: {}),
      throwsA(
        isA<ApiException>()
            .having((e) => e.statusCode, 'statusCode', 401)
            .having((e) => e.code, 'code', 'invalid_credentials'),
      ),
    );
  });
}
