"""Parses a model's raw text output into a tool-call proposal or plain content.

Extracted as a standalone, network-free function (not a method on
OllamaProvider) specifically so it can be unit-tested against the exact
response shapes observed from qwen2.5-coder:3b during the Gate 1 experiment
(docs/adr/0012-tool-calling-contract.md) without needing a real Ollama call
for every case: markdown-fenced JSON, unfenced JSON, unquoted values,
hallucinated tool names, missing required arguments, and plain prose.

This function does NOT grant any authority to what it parses — see
docs/07-agents/permissions.md. `UNKNOWN_TOOL` and `INVALID_ARGUMENTS` exist
so the caller can log/audit *why* a proposal was rejected, not to make the
proposal usable.
"""
import json
import re
from dataclasses import dataclass
from typing import Any

from app.ai.types import ToolCall, ToolCallOutcome, ToolDefinition

_FENCE_RE = re.compile(r"^```(?:json)?\s*(.*?)\s*```$", re.DOTALL)

_JSON_TYPE_MAP: dict[str, type | tuple[type, ...]] = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "object": dict,
    "array": list,
}


@dataclass(frozen=True)
class ParsedToolResponse:
    outcome: ToolCallOutcome
    tool_call: ToolCall | None
    raw_content: str
    reason: str | None = None


def _strip_fence(text: str) -> str:
    match = _FENCE_RE.match(text.strip())
    return match.group(1).strip() if match else text.strip()


def _validate_arguments(arguments: Any, schema: dict[str, Any]) -> str | None:
    """Minimal, hand-rolled JSON Schema subset check (required + basic type).

    Not a full JSON Schema implementation (no $ref, oneOf, etc.) — sufficient
    for the simple flat schemas used by iNOVA's Phase 1 tools. Revisit with
    the `jsonschema` package if a tool ever needs more than this.
    """
    if not isinstance(arguments, dict):
        return "arguments must be a JSON object"

    for required_key in schema.get("required", []):
        if required_key not in arguments:
            return f"missing required argument: {required_key}"

    properties: dict[str, Any] = schema.get("properties", {})
    for key, value in arguments.items():
        prop_schema = properties.get(key)
        if prop_schema is None:
            continue  # unknown extra argument — not flagged as invalid here
        expected_type = _JSON_TYPE_MAP.get(prop_schema.get("type", ""))
        if expected_type is not None and not isinstance(value, expected_type):
            return f"argument '{key}' should be of type {prop_schema.get('type')}"

        allowed_values = prop_schema.get("enum")
        if allowed_values is not None and value not in allowed_values:
            return f"argument '{key}' must be one of {allowed_values}, got {value!r}"

    return None


def parse_tool_response(content: str, offered_tools: list[ToolDefinition]) -> ParsedToolResponse:
    if not offered_tools:
        return ParsedToolResponse(ToolCallOutcome.NO_TOOL_CALL, None, content)

    candidate = _strip_fence(content)

    if not candidate.startswith("{"):
        return ParsedToolResponse(ToolCallOutcome.NO_TOOL_CALL, None, content)

    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError as exc:
        return ParsedToolResponse(ToolCallOutcome.MALFORMED, None, content, reason=str(exc))

    if not isinstance(parsed, dict) or "name" not in parsed or "arguments" not in parsed:
        return ParsedToolResponse(
            ToolCallOutcome.MALFORMED, None, content, reason="missing 'name' or 'arguments' key"
        )

    name = parsed["name"]
    arguments = parsed["arguments"]
    if not isinstance(name, str):
        return ParsedToolResponse(ToolCallOutcome.MALFORMED, None, content, reason="'name' is not a string")

    tool = next((t for t in offered_tools if t.name == name), None)
    if tool is None:
        return ParsedToolResponse(
            ToolCallOutcome.UNKNOWN_TOOL, None, content, reason=f"'{name}' is not in the offered tool list"
        )

    error = _validate_arguments(arguments, tool.input_schema)
    if error is not None:
        return ParsedToolResponse(ToolCallOutcome.INVALID_ARGUMENTS, None, content, reason=error)

    return ParsedToolResponse(ToolCallOutcome.VALID, ToolCall(name=name, arguments=arguments), content)
