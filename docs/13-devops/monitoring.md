# Monitoring

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how iNOVA's health is observed once it's running somewhere persistent.

## Scope

Application/infrastructure monitoring — not product analytics.

## Approach

`TODO — decision required` — Sentry or Grafana Cloud free tiers are sufficient at MVP scale (see [iNOVA_CAHIER_DES_CHARGES.md §5.2](../../iNOVA_CAHIER_DES_CHARGES.md)). Priority signals once implemented: API error rate, LLM inference latency (particularly relevant given local hardware constraints — see [06-ai/model-strategy.md](../06-ai/model-strategy.md)), agent tool-call failure rate.

## Related documentation

- [Logging](logging.md)
- [Model strategy](../06-ai/model-strategy.md)
