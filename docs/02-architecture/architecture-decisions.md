# Architecture Decisions

**Status:** Stable — index document
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Explain how architectural decisions are recorded for iNOVA, and point to the actual record.

## Scope

Process document. The decisions themselves live in [adr/](../adr/README.md).

## Why ADRs

iNOVA is built incrementally by design (see [product-philosophy.md](../00-overview/product-philosophy.md)). Without a record of *why* a technology or pattern was chosen, future contributors (human or AI) risk re-litigating settled decisions or, worse, silently violating them. Every hard-to-reverse technical choice gets a short ADR.

## What qualifies for an ADR

- Choice of a core technology (frontend framework, 3D engine, backend framework, LLM strategy).
- A cross-cutting pattern that constrains future code (e.g. agent permission model, provider abstraction).
- Anything that would be expensive to reverse later.

Small, easily-reversible implementation choices do not need an ADR.

## Current ADR index

See [adr/README.md](../adr/README.md) for the full list and status of each.

## Related documentation

- [Architecture overview](overview.md)
- [ADR index](../adr/README.md)
