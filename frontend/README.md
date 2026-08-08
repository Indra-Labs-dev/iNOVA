# iNOVA Frontend

Copyright (c) 2026 Archange Elie Yatte (AEY)

Flutter shell for iNOVA — Phase 0 Foundation scope only. See [../docs/ARCHITECTURE_FREEZE.md](../docs/ARCHITECTURE_FREEZE.md) and [../docs/03-frontend/architecture.md](../docs/03-frontend/architecture.md) for the full target architecture this scaffold implements a slice of.

## What's here (Phase 0)

- App shell, minimal routing (`core/routing/`), dark theme using the documented starting palette (`core/theme/`)
- One feature: `features/ai_chat/` — a screen that calls the backend's `POST /api/v1/ai/chat` and displays the response
- A static Aira placeholder (`shared/widgets/aira_placeholder.dart`) — **no Rive integration yet**, that's Phase 2

Everything else (3D world, real Aira state machine, other hubs) is `[PLANNED]` — see [../docs/16-roadmap/mvp.md](../docs/16-roadmap/mvp.md).

## Setup

Requires Flutter (stable channel). The backend (see `../backend/README.md`) must be running for the chat screen to get a real response — the app will show an error state otherwise, it won't crash.

```bash
flutter pub get
flutter run -d chrome --dart-define=API_BASE_URL=http://127.0.0.1:8010/api/v1
```

`API_BASE_URL` defaults to `http://127.0.0.1:8010/api/v1` if not passed (see `lib/core/config/app_config.dart`).

## Tests

```bash
flutter test
```

Covers: app boot/routing, the chat Riverpod controller (with a fake repository — no real backend needed), and the API client's error-envelope parsing (with a mocked HTTP client). See `../docs/14-testing/frontend-tests.md`.

## Project structure

```text
lib/
├── core/
│   ├── config/       compile-time app config (API base URL)
│   ├── theme/        iNova design tokens + ThemeData
│   ├── routing/      minimal named-route table
│   └── networking/   HTTP client + error envelope parsing
├── features/
│   └── ai_chat/      data (repository) / application (Riverpod controller) / presentation (screen)
├── shared/
│   └── widgets/      cross-feature widgets (incl. the Aira placeholder)
└── main.dart
```

See [../docs/03-frontend/architecture.md](../docs/03-frontend/architecture.md) for the target structure this will grow into (more `features/`, `nova/` → Aira module, `world/` for the 3D layer).
