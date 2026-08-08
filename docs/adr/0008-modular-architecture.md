# ADR-0008: Modular architecture over monolithic files/modules

**Status:** Accepted
**Date:** 2026-08-08

## Context

iNOVA's target scope spans 15+ functional modules ([08-modules/](../08-modules/ai-hub.md)), a 3D layer, a mascot, and an agent system. Built without discipline, this shape tends toward giant files and tightly coupled modules that become unmaintainable.

## Decision

Both frontend ([03-frontend/architecture.md](../03-frontend/architecture.md)) and backend ([02-architecture/components.md](../02-architecture/components.md)) are organized as small, cohesive, feature-scoped modules. Cross-module communication happens through shared core services or the event bus ([02-architecture/event-flow.md](../02-architecture/event-flow.md)), never direct imports between feature modules.

## Consequences

- New modules/agents can be added without rewriting the core, satisfying [00-overview/objectives.md](../00-overview/objectives.md) Objective 5 (extensibility).
- Slightly more upfront structure/boilerplate per module than a flat, ad hoc structure.
- Makes it easier to keep unfinished/`[PLANNED]` modules from entangling with modules already `[IMPLEMENTED]`.

## Alternatives considered

- A single shared codebase with feature flags and no strict module boundaries — rejected; the product's own philosophy explicitly warns against monolithic files and modules ([00-overview/product-philosophy.md](../00-overview/product-philosophy.md)).
