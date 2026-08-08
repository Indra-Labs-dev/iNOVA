# Network Security

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define network-level protections.

## Scope

Transport and network-layer concerns.

## Requirements

- TLS everywhere in production (see [13-devops/deployment.md](../13-devops/deployment.md) for cert management via Let's Encrypt).
- Rate limiting on public-facing endpoints, especially auth and AI endpoints (cost/abuse control given local LLM compute is finite — see [06-ai/model-strategy.md](../06-ai/model-strategy.md)).
- The local LLM host (Ollama) should not be exposed directly to the public internet — only the backend talks to it, on a private/internal network path.

## Related documentation

- [Security architecture](security-architecture.md)
- [Deployment](../13-devops/deployment.md)
