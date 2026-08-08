# Multimodal

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define what non-text input/output AI Core is expected to eventually support.

## Scope

Multimodal capability scope only — not yet implemented.

## Target capabilities (per product vision)

- Document analysis (uploaded files).
- Potential image understanding.

## Status note

Not started. The current model choice (`qwen2.5:3b-instruct`, text-only) does not support multimodal input — a multimodal-capable model or a separate specialized model would be required, which has additional VRAM implications on top of the constraints in [model-strategy.md](model-strategy.md). `TODO — decision required` when this capability is scheduled.

## Related documentation

- [Model strategy](model-strategy.md)
- [Architecture](architecture.md)
