# Animation Guidelines

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Keep Aira's motion purposeful and consistent with the rest of the product's motion language.

## Scope

Mascot-specific animation rules; the broader motion system is under [design-system.md](../03-frontend/design-system.md) (`iNovaMotion`).

## Rules

- Every animation must communicate state, not just decorate — no idle animation loop should be so busy it distracts from the current task.
- Respect reduced-motion accessibility settings: fall back to static state icons/poses rather than disabling Aira entirely (see [accessibility.md](../03-frontend/accessibility.md)).
- Transition timing between states should feel immediate for `thinking`/`listening` (low latency perception matters for conversational trust) and can be more expressive for `success`/`joy`.

## Related documentation

- [Rive](rive.md)
- [State machine](state-machine.md)
- [Accessibility](../03-frontend/accessibility.md)
