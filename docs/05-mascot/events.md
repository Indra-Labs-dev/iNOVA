# Events

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

List the concrete triggers Aira reacts to.

## Scope

Event catalog for the mascot specifically — the full application event catalog is in [02-architecture/event-flow.md](../02-architecture/event-flow.md).

## Triggers

Aira reacts to: AI state (thinking/responding), task completion, errors, alerts, achievements, direct user interactions (e.g. tapping Aira), and important system events (e.g. a critical watchlist item).

## Subscription model

Aira's state machine subscribes to the shared event bus rather than each feature calling into mascot code directly (see [state-machine.md](state-machine.md)).

## Related documentation

- [State machine](state-machine.md)
- [Event flow](../02-architecture/event-flow.md)
