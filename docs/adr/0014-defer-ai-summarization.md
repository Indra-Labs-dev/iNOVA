# ADR-0014: Defer AI summarization in News Intelligence — Gate 5 reliability findings

**Status:** Accepted
**Date:** 2026-08-08

## Context

[08-modules/news-intelligence.md](../08-modules/news-intelligence.md)'s MVP slice includes "basic RSS/API ingestion with AI summarization." [11-intelligence/summarization.md](../11-intelligence/summarization.md) states a hard product requirement: *"Summaries must clearly distinguish source facts, inference, opinion, and uncertainty... not a style preference."* Before writing `NewsService`, Gate 5 required a "Reality → Measurement" experiment — proving, against the real model actually available (`qwen2.5-coder:3b`), whether it can meet that requirement, before building persistence/API/frontend around an unproven capability.

## Experiment

9 real (non-mocked) calls to the local Ollama instance, one plain summarization prompt (2–3 sentences, facts only, hedge on inference, no invented names/dates/numbers — not iterated on after the fact), across 3 real RSS-sourced cases × 3 repeats: a near-zero-content item (hallucination-bait), a short item with concrete dates/times, and a real 1800-character technical article excerpt with concrete names/numbers.

## Findings

- **0/9 runs used any hedge language** ("it seems," "likely," etc.) despite explicit instruction — the model never distinguished stated fact from its own inference or added specificity, even when it invented unstated detail or introduced a factual error.
- **One direct factual inversion**: given a source stating a nomination period was the *"inaugural"* (first-ever) one, one run's summary called it the *"annual"* nominations — the opposite of what the source said, stated with full confidence, no hedge.
- **On thin content, consistent padding**: every run of the near-zero-content case invented generic specificity ("several bugs," "various issues," "issues identified in previous versions") not present in the 46-character source, stated as flat fact.
- **Omission was real and inconsistent between runs**: on the technical excerpt (source names 8 package ecosystems, cites "over 15,000 reports"), one run reported only 3 of 8 ecosystems and dropped the numeric fact entirely; the other two runs captured both far more completely — no run flagged that anything was omitted.
- **Same input, materially different output across repeats** — including the factual inversion above, which did not occur on the other two runs of the same case.
- One unprompted artifact: the system prompt's assistant persona ("You are Aira...") leaked into a summary's content itself (*"Aira, Dependabot expanded..."*) — a prompt-construction pitfall independent of the fact/inference finding, worth avoiding if this system-prompt pattern is reused for a future summarization task.
- Summary length and speed were not the problem — outputs were consistently short (1–3 sentences) and fast (~0.5–6.8s, cold-start included).

Full raw prompts/outputs are preserved in the Gate 5 session transcript; not reproduced verbatim here to keep this record focused on the decision.

## Decision

1. **AI summarization is deferred, not shipped**, for News Intelligence's Gate 5 slice. The pipeline is `Sources → Collection → Normalization → Persistence → Feed` — `NewsItem.title`/`excerpt` are always the source's own RSS text, verbatim (HTML-stripped and entity-unescaped for display, never paraphrased or generated).
2. **`NewsService` has no dependency on `AIService`/`LLMProvider` at all** — enforced structurally (its constructor accepts only repositories), not just by omission of a call, so no future change can silently reintroduce a model call into this pipeline without that being a visible, reviewable addition to the constructor signature.
3. **This is a measured result, not a hypothesis or a permanent architectural stance** — revisit only via a fresh, independent Reality → Measurement experiment (not by reusing this one's data) when the model strategy changes: a more capable local model, different hardware, or another validated strategy (see [06-ai/model-strategy.md](../06-ai/model-strategy.md)).
4. **Not fixed by adding a disclaimer.** A "may be inaccurate" label was considered and explicitly rejected as the shipped behavior — the measured failure (a confident factual inversion, not merely occasional vagueness) is a correctness problem a disclaimer doesn't solve for a feature meant to be a trustworthy digest.

## Consequences

- News Intelligence ships this Gate as `PARTIAL`: RSS ingestion, normalization, persistence, and source attribution are `IMPLEMENTED`/`TESTED`; AI summarization is `DEFERRED`; classification, semantic deduplication, cross-checking, and personalization remain `PLANNED` (Phase 5, untouched by this Gate).
- The user reads the source's own (sometimes terse) RSS description, not a synthesized summary — a real product-quality tradeoff, accepted deliberately over shipping a summarizer that can state a wrong fact with confidence.
- If a later Gate revisits this, the two things most worth re-testing first are exactly what failed here: the fact/inference hedging instruction, and stability across repeated runs on identical input — not just "does it produce a shorter sentence."

## Alternatives considered

- **Ship with a visible "AI-generated, may be inaccurate" disclaimer** — rejected: the measured failure mode is a model producing a confident, wrong statement (not hedged uncertainty), which a disclaimer doesn't meaningfully mitigate for a "trustworthy digest" product requirement.
- **Extractive/compressive summarization** (select and lightly compress source sentences rather than freely generate) — not implemented this Gate; documented in [11-intelligence/summarization.md](../11-intelligence/summarization.md) as a future avenue, explicitly requiring its own independent Reality → Measurement experiment before any implementation, not an extension of this one's results.
- **A more sophisticated prompt** to force the desired hedging behavior — explicitly rejected as a response to this experiment: papering over a measured reliability gap with prompt engineering was the one thing this Gate's instructions ruled out.
