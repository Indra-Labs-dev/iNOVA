# Frontend Architecture

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the Flutter application's internal structure so features stay isolated and the codebase stays navigable as modules are added.

## Scope

Flutter/Dart application structure. The 3D layer's internal structure is documented separately in [04-3d-world/architecture.md](../04-3d-world/architecture.md); it is embedded in, not owned by, the Flutter shell.

## Directory structure

```text
lib/
├── core/
│   ├── routing/
│   ├── theme/
│   ├── networking/
│   ├── storage/
│   ├── permissions/
│   └── design_system/
│
├── features/
│   ├── ai/
│   ├── agents/
│   ├── cybersecurity/
│   ├── programming/
│   ├── news/
│   ├── osint/
│   ├── learning/
│   ├── productivity/
│   ├── cloud/
│   └── devices/
│
├── nova/
│   ├── mascot/
│   ├── personality/
│   ├── emotions/
│   └── state_machine/
│
├── world/
│   ├── scene/
│   ├── objects/
│   ├── camera/
│   ├── effects/
│   └── interactions/
│
└── shared/
    ├── widgets/
    ├── animations/
    └── components/
```

## Rules

- A `feature/` module never imports another feature's internals directly — cross-feature communication goes through `core/` (events, shared state) or the backend API, never a direct Dart import between feature folders.
- `core/design_system/` is the only place allowed to define raw colors, spacing, and typography constants (see [design-system.md](design-system.md)).
- `world/` only receives data/events from `core/` — it does not know about specific features (e.g. it reacts to a generic `security.alert` event, not a `CybersecurityHub` class).
- No file should mix UI, business logic, and networking — see [state-management.md](state-management.md) for the intended separation via Riverpod.

## Related documentation

- [Flutter](flutter.md)
- [Riverpod](riverpod.md)
- [Design system](design-system.md)
- [Navigation](navigation.md)
- [State management](state-management.md)
