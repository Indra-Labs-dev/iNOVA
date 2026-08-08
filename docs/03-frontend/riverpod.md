# Riverpod

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how state management is structured so state doesn't leak between features or get duplicated.

## Scope

State management pattern only — see [state-management.md](state-management.md) for the broader philosophy.

## Conventions

- One provider scope per feature; providers live inside `features/<feature>/` next to the code that owns them, not centralized in one giant file.
- Shared/cross-cutting state (auth session, current user, permissions, theme) lives in `core/` providers.
- Async state (API calls, AI responses, agent execution status) uses `AsyncNotifier`/`AsyncValue` consistently so loading/error/data states are handled uniformly across the app, including by the mascot state machine (see [05-mascot/events.md](../05-mascot/events.md)) which listens to these states to drive its reactions.

## Related documentation

- [Architecture](architecture.md)
- [State management](state-management.md)
