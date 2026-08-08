# DataAgent

**Status:** [PLANNED] — Future
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Objective

Analyze structured/unstructured data the user provides or that other modules produce.

## Responsibilities

- Summarize and analyze datasets/documents.
- Surface patterns relevant to the user's request.

## Inputs

A dataset or document, an analysis question.

## Outputs

An analysis summary, optionally with visualizations `[FUTURE]`.

## Tools

- `analyze_document` — LOW risk.
- `query_dataset` — LOW to MEDIUM risk depending on data sensitivity.

## Permissions

`data.read`, scoped to data the user has uploaded or explicitly granted access to.

## Risks

LOW to MEDIUM — depends entirely on the sensitivity of the data being analyzed; no write access.

## Memory

Not persistent by default; analysis is per-request unless explicitly saved by the user.

## Dependencies

[LLMProvider](../../06-ai/llm-provider.md), [retrieval](../../06-ai/retrieval.md), object storage.

## Events

`agent.task.succeeded/failed`.

## Errors

Corrupted/unreadable file → report clearly, do not guess content.

## Confirmation

Not required for read-only analysis.

## Audit

Data access logged per [audit.md](../audit.md), respecting [data-protection.md](../../12-security/data-protection.md).

## Related documentation

- [Retrieval](../../06-ai/retrieval.md)
- [Data protection](../../12-security/data-protection.md)
