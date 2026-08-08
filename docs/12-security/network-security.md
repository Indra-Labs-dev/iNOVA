# Network Security

**Status:** [PARTIAL] — CORS policy implemented in Phase 0; SSRF prevention implemented in Gate 2 (`read_rss_feed`)
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

## SSRF prevention — implemented (Gate 2)

The first tool with real network access (`read_rss_feed`, [ResearchAgent](../07-agents/agents/research-agent.md)) is designed so the model **never supplies a URL**: its only input is `feed_id`, constrained by JSON Schema `enum` to a small, hardcoded, server-side allowlist (`backend/app/tools/research_tools.py::RSS_ALLOWLIST`). The handler resolves `feed_id` → URL itself; no argument from the model ever becomes part of the outbound request URL, so there is no code path through which a hallucinated or adversarial value (`http://169.254.169.254/...`, `http://localhost:...`, `http://10.x.x.x`, etc.) can reach the network layer — this is checked defensively at two layers: the JSON Schema `enum` (rejected as `INVALID_ARGUMENTS` before execution) and again inside the handler itself (never trust that upstream validation was the only gate). `follow_redirects=False` additionally prevents an allowlisted feed from redirecting the request off-allowlist. See `backend/tests/test_research_tools.py::test_url_smuggled_as_feed_id_is_rejected_without_any_network_call` for the regression test.

## Related documentation

- [Security architecture](security-architecture.md)
- [Deployment](../13-devops/deployment.md)
- [ResearchAgent](../07-agents/agents/research-agent.md)
