# ADR-0003: Rive for the mascot

**Status:** Accepted
**Date:** 2026-08-08

## Context

Aira ([05-mascot/](../05-mascot/overview.md)) needs a state-machine-driven animation system that's lightweight enough for a 2D UI context and expressive enough to carry emotional/functional meaning across 13 states ([05-mascot/states.md](../05-mascot/states.md)).

## Decision

Rive is used for Aira's interactive state machine; Lottie is used only for supplementary one-off effects, not the mascot's core states.

## Consequences

- A single Rive artifact can encode the full state machine, keeping transitions centrally controlled (see [05-mascot/rive.md](../05-mascot/rive.md)).
- Rive's free tier covers individual/small-team use; collaborative team plans are paid (see [iNOVA_CAHIER_DES_CHARGES.md §5.4](../../iNOVA_CAHIER_DES_CHARGES.md)).
- Requires a Flutter Rive runtime dependency.

## Alternatives considered

- Lottie for everything — rejected as primary because Lottie lacks Rive's native interactive state-machine model, which is central to how Aira's states are meant to be driven by application events.
- Hand-rolled Flutter animations — much higher implementation cost for comparable expressiveness.
