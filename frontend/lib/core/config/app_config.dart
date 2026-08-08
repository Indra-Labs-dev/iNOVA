// Compile-time configuration via --dart-define, see docs/12-security/secrets.md:
// no secret belongs here — only the API base URL, which is not sensitive.
class AppConfig {
  const AppConfig._();

  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://127.0.0.1:8010/api/v1',
  );
}
