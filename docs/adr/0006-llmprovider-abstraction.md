# ADR-0006: LLMProvider abstraction

**Status:** Accepted
**Date:** 2026-08-08

## Context

The product vision requires supporting multiple AI providers and forbids hard-coding around one ([00-overview/objectives.md](../00-overview/objectives.md), Objective 2). The current setup uses a local model chosen under hardware constraints ([ADR-0005](0005-ollama-local-llm.md)) that may change.

## Decision

AI Core and all agents interact with model backends exclusively through an `LLMProvider` interface ([06-ai/llm-provider.md](../06-ai/llm-provider.md)). No agent or AI Core code imports a provider-specific client directly.

## Consequences

- Switching from Ollama to a bigger local model or a cloud provider later requires only a new `LLMProvider` implementation, not changes to agent logic.
- Adds a small amount of upfront abstraction overhead compared to calling Ollama's API directly.
- Makes ADR-0005 cheap to reverse — this is the primary reason the two ADRs are paired.

## Alternatives considered

- Direct Ollama API calls throughout the codebase — rejected: would silently lock the entire agent system to the local-only setup, contradicting the multi-provider requirement in the product vision.
