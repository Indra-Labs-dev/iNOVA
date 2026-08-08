// Minimal in-memory auth session — deliberately not persisted (no secure
// storage integration yet) and not a full auth feature: just enough for
// features/research/ to authenticate its calls, per docs/adr/0010's
// in-house JWT contract. A real login/session feature with token
// persistence is future work, not part of this Gate.
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../networking/api_client.dart';

class AuthSession {
  const AuthSession({this.accessToken, this.email});

  final String? accessToken;
  final String? email;

  bool get isAuthenticated => accessToken != null;
}

class AuthSessionController extends Notifier<AuthSession> {
  @override
  AuthSession build() => const AuthSession();

  Future<void> login(String email, String password) async {
    final client = ref.read(apiClientProvider);
    final response = await client.postJson(
      '/auth/login',
      body: {'email': email, 'password': password},
    );
    state = AuthSession(accessToken: response['access_token'] as String, email: email);
  }
}

final authSessionProvider = NotifierProvider<AuthSessionController, AuthSession>(
  AuthSessionController.new,
);
