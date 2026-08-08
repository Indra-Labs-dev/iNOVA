# Conventions

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Set baseline coding conventions ahead of the first real code, so style questions don't get re-litigated per PR.

## Scope

Cross-cutting conventions. Language-specific detail expands here once code exists.

## General rules (from product philosophy, see [00-overview/product-philosophy.md](../00-overview/product-philosophy.md))

- No giant files; keep modules cohesive.
- Typed models and explicit interfaces everywhere (Dart null-safety, Python type hints + Pydantic).
- Separate UI, business logic, data access, and infrastructure.
- No duplicated functionality — check for an existing implementation before adding a new one.
- No comments explaining *what* code does; only *why*, when non-obvious.

## Related documentation

- [Product philosophy](../00-overview/product-philosophy.md)
- [Code review](code-review.md)
- [Dependency policy](dependency-policy.md)
