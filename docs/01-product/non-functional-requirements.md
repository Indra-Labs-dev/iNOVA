# Non-Functional Requirements

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the quality bar iNOVA must meet regardless of which feature is being built.

## Scope

Cross-cutting constraints referenced by every module doc.

## Security

- Authentication and authorization implemented from the first working version, never retrofitted.
- No AI/agent output executed without validation (see [agent-security.md](../12-security/agent-security.md)).
- Secrets never stored in source code (see [secrets.md](../12-security/secrets.md)).
- All transport encrypted (TLS).

## Performance

- 3D world must degrade gracefully on low-end GPUs (see [04-3d-world/performance.md](../04-3d-world/performance.md)).
- Local LLM inference latency must be surfaced to the user via mascot state (`thinking`/`working`), never silently blocking the UI.
- API responses for non-AI endpoints should target sub-300ms at the MVP scale.

## Accessibility

- Reduced-motion setting must be respected across mascot, 3D world, and UI transitions.
- Color choices must maintain readable contrast even within the "futuristic/glass" design language (see [design-system.md](../03-frontend/design-system.md)).

## Maintainability

- No monolithic files; features split into small, cohesive components (see [product-philosophy.md](../00-overview/product-philosophy.md)).
- Every significant architectural decision recorded as an ADR (see [adr/README.md](../adr/README.md)).

## Reliability

- Agent tool calls must fail safely: an invalid or malformed tool call must be rejected and logged, never partially executed.
- Local LLM constraints (4GB VRAM today) must be treated as a documented, revisable constraint, not baked into the architecture as a permanent limitation (see [06-ai/model-strategy.md](../06-ai/model-strategy.md)).

## Privacy

- Personalization features must be opt-in and explainable.
- Device/system access (Device Hub, Cloud Hub) strictly permission-gated.

## Related documentation

- [Functional requirements](functional-requirements.md)
- [Security architecture](../12-security/security-architecture.md)
- [Testing strategy](../14-testing/strategy.md)
