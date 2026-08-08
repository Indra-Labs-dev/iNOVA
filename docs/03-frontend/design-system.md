# Design System

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Centralize the visual language so iNOVA's futuristic identity stays consistent instead of scattering constants across features.

## Scope

Design tokens and shared component contracts. Actual pixel-level design work happens in design tooling; this document tracks the system as code needs to implement it.

## Design tokens

```text
iNovaColors
iNovaTypography
iNovaSpacing
iNovaRadius
iNovaShadows
iNovaGlass
iNovaMotion
```

## Starting palette

| Name | Hex |
|---|---|
| Deep Space | `#07111F` |
| Electric Blue | `#0066FF` |
| Cyan | `#20D9FF` |
| Purple | `#8B5CFF` |
| Neon Orange | `#FF5A1F` |
| White | `#F5F8FF` |

These are starting values, not immutable brand rules — expect refinement once real screens are built.

## Shared components

```text
NovaCard
NovaButton
NovaPanel
NovaGlass
NovaOrb
NovaHologram
NovaMetric
NovaBadge
NovaDialog
NovaCommandBar
NovaAgentCard
```

Each component should be documented with its states (default, hover, disabled, loading, error) once implemented — add a per-component page under this folder when the component moves to `[IN PROGRESS]`, rather than pre-writing specs for unimplemented components.

**Naming note:** this `Nova*` prefix is a design-token/component-library naming convention (like `iNovaColors`, `iNovaMotion` above), independent from the mascot's identity. It predates the mascot naming decision ([ADR-0009](../adr/0009-mascot-naming-aira.md): the mascot is officially **Aira**, not Nova). Whether to rename this component prefix for consistency (e.g. `AiraCard`) or keep it as a distinct design-system brand token is an open decision — `TODO — decision required`, not resolved by this review, since it affects a components no other document currently ties to the mascot's character identity.

## Design intent

Futuristic, premium, clean, immersive, intelligent, slightly cyberpunk, readable, accessible. Explicitly avoid the generic "neon hacker dashboard" look — the futuristic aesthetic must be carried by strong UX and hierarchy, not just color.

## Related documentation

- [Architecture](architecture.md)
- [Accessibility](accessibility.md)
- [Mascot animation guidelines](../05-mascot/animation-guidelines.md)
