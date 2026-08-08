# Retrieval

**Status:** [PLANNED]
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define how AI Core grounds responses in external or internal data rather than relying purely on model knowledge.

## Scope

Retrieval mechanism. Source-level ingestion policy is in [11-intelligence/ingestion.md](../11-intelligence/ingestion.md).

## Use cases

- Answering questions using ingested news/research content (see [11-intelligence/](../11-intelligence/ingestion.md)).
- Grounding agent decisions in the [Knowledge Graph](../08-modules/knowledge-graph.md) once it exists.
- Document analysis: retrieving relevant chunks of a user-uploaded document.

## Status note

`[PLANNED]` — no retrieval mechanism exists yet; this document defines intended scope so a vector store / embedding strategy isn't chosen ad hoc later without considering the 4GB VRAM constraint (embeddings can be computed with a small dedicated embedding model rather than the chat model — `TODO — decision required` on which one).

## Related documentation

- [Context management](context-management.md)
- [Knowledge Graph](../08-modules/knowledge-graph.md)
- [Ingestion](../11-intelligence/ingestion.md)
