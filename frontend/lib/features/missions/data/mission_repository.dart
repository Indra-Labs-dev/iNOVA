// Calls POST /api/v1/missions — see docs/08-modules/mission-system.md and
// docs/09-backend/api-design.md. Requires an access token (docs/adr/0010).
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/networking/api_client.dart';
import 'mission_result.dart';

class MissionRepository {
  MissionRepository(this._client);

  final ApiClient _client;

  Future<MissionResult> start(String goal, {required String accessToken}) async {
    final response = await _client.postJson(
      '/missions',
      body: {'goal': goal},
      authToken: accessToken,
    );
    return MissionResult.fromJson(response);
  }
}

final missionRepositoryProvider = Provider<MissionRepository>(
  (ref) => MissionRepository(ref.watch(apiClientProvider)),
);
