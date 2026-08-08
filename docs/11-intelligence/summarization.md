# Summarization

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how AI-generated summaries are produced and constrained.

## Scope

Post-classification step, before source attribution is attached.

## Requirement

Summaries must clearly distinguish source facts, inference, opinion, and uncertainty (see [08-modules/news-intelligence.md](../08-modules/news-intelligence.md)). This is a hard product requirement, not a style preference — it directly affects user trust.

## Dependency

Uses [LLMProvider](../06-ai/llm-provider.md); summary quality is bounded by the current local model's capability (see [06-ai/model-strategy.md](../06-ai/model-strategy.md)).

## Related documentation

- [Classification](classification.md)
- [Source attribution](source-attribution.md)
