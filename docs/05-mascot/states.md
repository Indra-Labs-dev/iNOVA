# States

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Enumerate every visual state Aira must support.

## Scope

State catalog only; transition logic is in [state-machine.md](state-machine.md), triggers are in [events.md](events.md).

## Full state set

```text
idle
welcome
thinking
listening
speaking
working
success
joy
error
warning
waiting
loading
incoming_event
```

## MVP subset

Per [16-roadmap/mvp.md](../16-roadmap/mvp.md), only `idle`, `thinking`, `speaking`, `success`, and `error` are required for the first working version. The remaining states are `[PLANNED]` for Phase 2.

## Related documentation

- [State machine](state-machine.md)
- [Events](events.md)
- [Animation guidelines](animation-guidelines.md)
