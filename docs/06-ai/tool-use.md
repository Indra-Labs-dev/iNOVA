# Tool Use

**Status:** [PARTIAL] — mechanical contract implemented and measured (Gate 1); no agent consumes it yet
**Owner:** Archange Elie Yatte
**Last Updated:** 2026-08-08

## Purpose

Define the contract for how AI Core and agents invoke tools — the mechanism that turns "AI beyond chat" (Objective 2) into something safe.

## Scope

Tool-calling contract. Permission enforcement is documented in [07-agents/permissions.md](../07-agents/permissions.md) and [12-security/agent-security.md](../12-security/agent-security.md) — this document covers the mechanical contract only.

## Contract

1. The model receives a list of available tools with their JSON schema (name, description, parameters) — scoped to what's permitted for the current user/context, not a global list.
2. If the model requests a tool call, the backend validates it against the tool's schema **before** anything else happens.
3. An invalid or malformed tool call is rejected and logged — never partially executed, never silently corrected by guessing intent.
4. A valid tool call still passes through the permission check and confirmation gate defined in [07-agents/permissions.md](../07-agents/permissions.md) before execution.

## Reliability — measured, not assumed (Gate 1)

The reliability note below was a prediction; it has now been tested against real Ollama calls with `qwen2.5-coder:3b` — see [ADR-0012](../adr/0012-tool-calling-contract.md) for the full experiment and data. Headline results:

- 100% reliable (format, tool name, argument) when the request clearly matches the one offered tool and its argument is explicit in the user's message.
- 100% tool-name hallucination when no offered tool actually matches the request — the model invents a plausible tool name rather than declining.
- The model never uses Ollama's native structured `tool_calls` response field — every proposal must be parsed from free-text `content`, including handling markdown code fences and outright malformed JSON.

Step 3 above (validate before anything else happens) is therefore not optional hardening — this experiment is direct evidence it is load-bearing: it is what turns 100% hallucination-on-mismatch into zero actual risk, since a proposal naming an unregistered tool is simply rejected. See [tool_call_parsing.py](../../backend/app/ai/tool_call_parsing.py) (discriminated outcomes: `VALID`/`MALFORMED`/`UNKNOWN_TOOL`/`INVALID_ARGUMENTS`/`NO_TOOL_CALL`) for the implementation this maps to.

## Related documentation

- [LLMProvider](llm-provider.md)
- [Model strategy](model-strategy.md)
- [Agent permissions](../07-agents/permissions.md)
- [Agent security](../12-security/agent-security.md)
- [ADR-0012: Tool-calling contract](../adr/0012-tool-calling-contract.md)
