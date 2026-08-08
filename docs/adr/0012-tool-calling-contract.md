# ADR-0012: Tool-calling contract shape and Gate 1 reliability findings

**Status:** Accepted
**Date:** 2026-08-08

## Context

[06-ai/llm-provider.md](../06-ai/llm-provider.md) documented a conceptual `generate(messages, tools?) -> completion | tool_call` contract but left it unimplemented. Before building `ResearchAgent` (Phase 1), the [Phase 1 plan](../PROJECT_STATUS.md) required a "Gate 1" experiment to prove — empirically, against the real model actually available (`qwen2.5-coder:3b`, see [ADR-0005 addendum](0005-ollama-local-llm.md)) — whether native LLM tool-calling is reliable enough to build on, before writing `ResearchAgent`, `AuditLog`, or a `Tool Registry` around an unproven mechanism.

## Experiment

~21 real (non-mocked) calls to the local Ollama instance, `qwen2.5-coder:3b`, with a single synthetic tool (`read_rss_feed`) offered, across three batches: baseline prompts (no system guidance), repeated-trial consistency checks, and a batch with a system prompt guiding the model on when to (not) propose a tool call.

## Findings

- **Ollama's native `message.tool_calls` field was never populated (0/21)** — this model/template combination always emits its tool-call proposal as JSON text inside `message.content`, sometimes wrapped in a markdown code fence (` ```json ... ``` `), sometimes not. Any implementation relying on the structured field alone would see zero tool calls, ever.
- **100% reliable (8/8) on the narrow target scenario**: a request that clearly matches the one offered tool, with the required argument explicit in the user's message (e.g. "read this RSS feed: `<url>`") — correct tool name, correct argument, valid JSON (after fence-stripping), every time, including 5 repeated identical trials.
- **100% tool-name hallucination (4/4) when no offered tool matches the request** (math, greeting, general knowledge) — the model invented plausible-sounding tool names never offered (`calculate`, `greet`, `search_online`, `research_latest_ai_news`). A system prompt explicitly instructing "only propose a tool call if it matches your one tool" measurably reduced this (2/3 clean plain-text answers) but did not eliminate it, and introduced a new failure mode in the process (see below).
- **Argument fabrication**: when the tool was correctly selected but no concrete value was given by the user (e.g. "read the RSS feed" with no URL), the model invented a plausible-looking URL in 100% of such cases (4/4) rather than asking for clarification.
- **One genuine JSON syntax error observed** (with the system-prompt variant): `{"name": read_rss_feed, "arguments": {...}}` — the name value emitted unquoted, invalid JSON. Rare (1/21) but real — a naive parser must never assume the model's JSON is well-formed.
- **No-tools baseline behaves normally**: without a `tools` param, the same model answers in fluent natural language — the JSON-forcing behavior is specifically tied to the presence of `tools` in the request.

Full data and raw response strings are used verbatim as test fixtures in `backend/tests/test_tool_call_parsing.py`.

## Decision

1. **`LLMProvider.generate(message, tools=None) -> LLMResponse`** (`LLMResponse` = `{content: str|None, tool_call: ToolCall|None}`), implemented in `OllamaProvider` only — `OllamaProvider` remains the sole place aware of Ollama's actual wire behavior (fence-wrapped JSON-in-content, not the native field).
2. **Tool-call parsing is a standalone, unit-testable function** (`app/ai/tool_call_parsing.py::parse_tool_response`), not inlined in `OllamaProvider`, with a discriminated outcome (`VALID`, `MALFORMED`, `UNKNOWN_TOOL`, `INVALID_ARGUMENTS`, `NO_TOOL_CALL`) so failure modes are distinguishable for future audit logging.
3. **Strategy: NATIVE TOOL CALLING**, not a deterministic backend-selection fallback — justified specifically for Phase 1's narrow scope (one tool, invoked only when the request context makes the tool and its arguments unambiguous). This is not a general endorsement of this model's tool-calling for arbitrary multi-tool, multi-intent use.
4. **Strict backend validation is not optional hardening — it is the load-bearing safety mechanism**, empirically justified by this experiment: every hallucinated tool name and every malformed response is rendered harmless by validating the proposal against the real tool registry before execution, per [07-agents/permissions.md](../07-agents/permissions.md) ("never execute a tool call solely because the model requested it"). The LLM proposes; the backend decides — this experiment is evidence for why, not just policy.
5. **Argument fabrication risk carried forward as a design requirement for Gate 2**: `read_rss_feed`'s `feed` argument must be validated against a concrete allowlist server-side (already planned), since the model will invent a plausible-but-arbitrary URL when the user doesn't supply one.

## Consequences

- `AIService.chat()` (Phase 0's `/api/v1/ai/chat`) keeps its `str` return contract via a thin wrapper (`generate(message).content or ""`) — no breaking change to the existing endpoint.
- Multi-tool discrimination (does the model pick correctly among *several* real tools, not just "one tool, relevant or not") is **untested** — this experiment only offered one tool at a time. Re-run an equivalent Gate before Phase 4's Agent Router work adds a second agent/tool.
- The markdown-fence + malformed-JSON handling in `parse_tool_response` is model-specific behavior, not a documented Ollama guarantee — revisit if the configured model tag changes (see [ADR-0005 addendum](0005-ollama-local-llm.md)).

## Alternatives considered

- **Deterministic backend tool selection** (skip LLM-driven tool choice entirely) — rejected for Phase 1: the data shows native calling is reliable for the actual target scenario, and choosing determinism now would mean never actually validating the "AI beyond chat" tool-use contract this phase exists to prove.
- **Trusting Ollama's native `tool_calls` field** — rejected: empirically unused by this model, would silently produce zero tool calls.
