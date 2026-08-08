# Threat Model

**Status:** [PLANNED] — initial pass, to be revisited per module as each is implemented
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Enumerate the realistic threats iNOVA's design must account for, given its specific shape (AI agents with tool access, local LLM, multi-module platform).

## Scope

High-level threat categories. Mitigations are detailed in their respective documents.

## Key threats

| Threat | Primary mitigation |
|---|---|
| AI hallucinates/malforms a tool call, causing unintended action | Strict server-side validation, never trust model output ([agent-security.md](agent-security.md), [06-ai/tool-use.md](../06-ai/tool-use.md)) |
| Agent performs a high-impact action without real user awareness | Mandatory confirmation gates on HIGH-risk tools ([07-agents/permissions.md](../07-agents/permissions.md)) |
| Secrets leaked via source code or logs | Secret management discipline ([secrets.md](secrets.md)) |
| Unauthorized access to another user's data | Scoped authorization on every endpoint ([authorization.md](authorization.md)) |
| Cybersecurity/OSINT Hub misused for offensive purposes against third parties | Hard product boundary: authorized/owned systems only ([08-modules/cybersecurity-hub.md](../08-modules/cybersecurity-hub.md)) |
| Ingestion pipeline used to bypass site protections | Explicit scraping policy ([11-intelligence/scraping-policy.md](../11-intelligence/scraping-policy.md)) |
| Local LLM's lower reliability leads to more frequent malformed agent actions | Treated as an active risk factor, not just noise — see [06-ai/model-strategy.md](../06-ai/model-strategy.md) consequences section |
| Sensitive local data (device, files) exposed without consent | Strict permission gating on Device/Cloud Hub ([08-modules/device-hub.md](../08-modules/device-hub.md)) |

## Related documentation

- [Security architecture](security-architecture.md)
- [Agent security](agent-security.md)
