# State Management

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the layering discipline between UI, application state, and data access on the frontend.

## Scope

Frontend-only. Backend state/data layering is in [02-architecture/components.md](../02-architecture/components.md) and [10-data/](../10-data/data-architecture.md).

## Layers

```text
Widget (UI)
   |
Riverpod Notifier/Provider (application state)
   |
Repository (API/WebSocket access)
   |
Backend API
```

- Widgets read state and dispatch intents; they never call repositories directly (see [riverpod.md](riverpod.md)).
- Repositories are the only layer aware of HTTP/WebSocket details.
- Real-time state (agent execution progress, mascot events) flows through a WebSocket-backed provider, not polling.

## Related documentation

- [Riverpod](riverpod.md)
- [Architecture](architecture.md)
- [WebSocket](../09-backend/websocket.md)
