# Rive

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Record the decision and implementation approach for using Rive as Aira's animation technology.

## Scope

Rive-specific integration. See [adr/0003-rive-mascot.md](../adr/0003-rive-mascot.md) for rationale.

## Approach

- Aira's states ([states.md](states.md)) map to a single Rive state machine artifact, not separate disconnected animation files, so transitions stay smooth and centrally controlled.
- Lottie is used only for supplementary one-off effects, not for Aira's core states (see [animation-guidelines.md](animation-guidelines.md)).

## External dependency note

Rive's editor is free for individual/small-team use; collaborative team plans are paid. See [iNOVA_CAHIER_DES_CHARGES.md](../../iNOVA_CAHIER_DES_CHARGES.md) §5.4 for cost detail.

## Related documentation

- [State machine](state-machine.md)
- [Animation guidelines](animation-guidelines.md)
