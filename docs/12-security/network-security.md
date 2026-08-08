# Network Security

**Status:** [PARTIAL] — CORS policy implemented in Phase 0 (`backend/app/main.py`)
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define network-level protections.

## Scope

Transport and network-layer concerns.

## Requirements

- TLS everywhere in production (see [13-devops/deployment.md](../13-devops/deployment.md) for cert management via Let's Encrypt).
- Rate limiting on public-facing endpoints, especially auth and AI endpoints (cost/abuse control given local LLM compute is finite — see [06-ai/model-strategy.md](../06-ai/model-strategy.md)). `[PLANNED]`, not implemented in Phase 0.
- The local LLM host (Ollama) should not be exposed directly to the public internet — only the backend talks to it, on a private/internal network path.

## CORS policy — implemented

`flutter run -d chrome` / a static web build can land on an arbitrary localhost port, making a fixed origin allowlist impractical for local development. The Phase 0 implementation therefore branches on `settings.environment`:

- **development**: `allow_origin_regex` scoped to `http://(localhost|127.0.0.1)(:port)?` — permissive, but only for loopback addresses, never a wildcard `*` origin.
- **staging/production**: falls back to `settings.cors_origins`' explicit allowlist — no regex, no loopback leniency.

This was discovered as a real integration bug during Phase 0 (the Flutter web build was blocked by the CORS preflight against the documented static origin list) and fixed directly rather than left as a `TODO`, since it was required for the MVP success criteria's frontend↔backend integration to actually work.

## Related documentation

- [Security architecture](security-architecture.md)
- [Deployment](../13-devops/deployment.md)
