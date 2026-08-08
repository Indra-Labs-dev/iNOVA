# Summarization

**Status:** [DEFERRED] — measured against the real model and found unreliable, see [ADR-0014](../adr/0014-defer-ai-summarization.md)
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08 (Gate 5 — Extractive News Digest)

## Purpose

Define how AI-generated summaries are produced and constrained.

## Scope

Post-classification step, before source attribution is attached.

## Requirement

Summaries must clearly distinguish source facts, inference, opinion, and uncertainty (see [08-modules/news-intelligence.md](../08-modules/news-intelligence.md)). This is a hard product requirement, not a style preference — it directly affects user trust.

## Gate 5 measurement — deferred, not implemented

Before writing `NewsService`, a real experiment (9 calls, real `qwen2.5-coder:3b`, real RSS content, one plain prompt not iterated on afterward) measured this requirement directly. Result: **0/9 runs hedged inference as instructed**, and one run produced a direct factual inversion ("inaugural" → "annual") stated with full confidence. Full findings and the decision they led to are in [ADR-0014](../adr/0014-defer-ai-summarization.md) — this is a measured result, not an assumption, and not something a more careful prompt was allowed to paper over per the Gate 5 instructions.

Gate 5 ships an **extractive digest** instead: `NewsItem.title`/`excerpt` are always the source's own RSS text, verbatim (HTML-stripped, entities unescaped — normalization only, never a paraphrase).

## Future avenue — not implemented, needs its own measurement

An extractive/compressive approach (select and lightly compress 1–2 sentences directly from the source text, no free-form generation) is documented here as a candidate worth exploring later — closer to extraction than generation, which might reduce the invention risk this Gate measured. It has **not** been tested and must not be assumed to work; if pursued, it requires its own independent Reality → Measurement experiment before any implementation, not an extension of Gate 5's data.

## Dependency

Uses [LLMProvider](../06-ai/llm-provider.md); summary quality is bounded by the current local model's capability (see [06-ai/model-strategy.md](../06-ai/model-strategy.md)) — this is exactly the constraint Gate 5 measured and found insufficient for this task, at this model size, today.

## Related documentation

- [Classification](classification.md)
- [Source attribution](source-attribution.md)
- [ADR-0014: Defer AI summarization](../adr/0014-defer-ai-summarization.md)
