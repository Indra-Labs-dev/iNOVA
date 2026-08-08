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

  test('getJson returns a decoded list for list endpoints', () async {
    final mockClient = MockClient((request) async {
      expect(request.method, 'GET');
      return http.Response(jsonEncode([{'id': '1'}, {'id': '2'}]), 200);
    });
    final client = ApiClient(httpClient: mockClient, baseUrl: 'http://test');

    final result = await client.getJson('/conversations', authToken: 'tok');

    expect(result, [
      {'id': '1'},
      {'id': '2'},
    ]);
  });

  test('getJson throws ApiException parsed from the error envelope', () async {
    final mockClient = MockClient((request) async {
      return http.Response(
        jsonEncode({
          'error': {'code': 'not_authenticated', 'message': 'Missing token.', 'details': null}
        }),
        401,
      );
    });
    final client = ApiClient(httpClient: mockClient, baseUrl: 'http://test');

    expect(
      () => client.getJson('/conversations'),
      throwsA(isA<ApiException>().having((e) => e.statusCode, 'statusCode', 401)),
    );
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
