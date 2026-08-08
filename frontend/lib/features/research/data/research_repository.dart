// Calls POST /api/v1/agents/research — see
// docs/07-agents/agents/research-agent.md and docs/09-backend/api-design.md.
// Requires an access token (docs/adr/0010) — see core/auth/auth_session.dart.
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/networking/api_client.dart';
import 'research_result.dart';

class ResearchRepository {
  ResearchRepository(this._client);

  final ApiClient _client;

  Future<ResearchResult> research(String query, {required String accessToken}) async {
    final response = await _client.postJson(
      '/agents/research',
      body: {'query': query},
      authToken: accessToken,
    );
    return ResearchResult.fromJson(response);
  }
}

final researchRepositoryProvider = Provider<ResearchRepository>(
  (ref) => ResearchRepository(ref.watch(apiClientProvider)),
);
