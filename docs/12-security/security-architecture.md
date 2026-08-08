# Security Architecture

**Status:** [PLANNED] — priority document
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Give the top-level picture of how security is built into iNOVA from day one, and index the rest of `12-security/`.

## Scope

Cross-cutting security architecture. Agent-specific detail is in [agent-security.md](agent-security.md).

## Non-negotiable baseline (from the product vision)

Implemented from the beginning, never retrofitted: authentication, authorization, scoped permissions, secure sessions, encrypted transport, secret management, input validation, output validation, audit logging, rate limiting, agent permission boundaries, tool allowlists, confirmation gates, safe defaults, data deletion controls.

**AI agents are treated as potentially untrusted decision-makers. Model output is never executed blindly.**

## Document map

| Concern | Document |
|---|---|
| What could go wrong | [threat-model.md](threat-model.md) |
| Identity | [authentication.md](authentication.md) |
| What identity can do | [authorization.md](authorization.md) |
| Agent-specific boundaries | [agent-security.md](agent-security.md) |
| Secret handling | [secrets.md](secrets.md) |
| Network posture | [network-security.md](network-security.md) |
| Data at rest/in transit | [data-protection.md](data-protection.md) |
| Traceability | [audit-logging.md](audit-logging.md) |
| Process | [secure-development.md](secure-development.md) |
| When something goes wrong | [incident-response.md](incident-response.md) |

## Related documentation

- [Product philosophy](../00-overview/product-philosophy.md)
- [Non-functional requirements](../01-product/non-functional-requirements.md)
