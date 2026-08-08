# OSINTAgent

**Status:** [PLANNED] — Future (after Phase 6)
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Objective

Collect and correlate public-source information for legitimate research, defensive security, or authorized investigation.

## Responsibilities

- Gather DNS, public certificate, domain metadata, and public reputation information.
- Correlate findings with news/threat intelligence.

## Inputs

A public entity to investigate (domain, public identifier) with a stated legitimate purpose.

## Outputs

A structured public-intelligence summary with source attribution.

## Tools

- `dns_lookup` — LOW risk.
- `certificate_lookup` — LOW risk.
- `domain_metadata_lookup` — LOW risk.

All tools restricted to public, passive data sources — see [osint-hub.md](../../08-modules/osint-hub.md) boundaries.

## Permissions

`osint.read`, scoped to public data only.

## Risks

LOW — passive/public data only. No permission to actively probe or exploit systems.

## Memory

Investigation-scoped; not merged into general user memory without explicit action.

## Dependencies

[LLMProvider](../../06-ai/llm-provider.md), external OSINT data providers (see [iNOVA_CAHIER_DES_CHARGES.md §5.2](../../../iNOVA_CAHIER_DES_CHARGES.md) for cost/quota notes).

## Events

`agent.task.succeeded/failed`.

## Errors

Provider quota exceeded or unavailable → fail cleanly, no fallback to unauthorized methods.

## Confirmation

Not required — read-only, public data.

## Audit

Every lookup and its source logged per [audit.md](../audit.md).

## Related documentation

- [OSINT Hub](../../08-modules/osint-hub.md)
- [Scraping policy](../../11-intelligence/scraping-policy.md)
