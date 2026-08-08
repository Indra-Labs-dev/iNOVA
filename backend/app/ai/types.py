"""Shared types for the LLMProvider tool-calling contract.

See docs/06-ai/llm-provider.md (`generate(message, tools?) -> LLMResponse`)
and docs/07-agents/tools.md for the tool definition shape. `permission`/
`risk`/`confirmation_required` are carried on `ToolDefinition` per
docs/07-agents/permissions.md, but no permission *system* (registry storage,
grants) is built yet — see docs/16-roadmap/phases.md Phase 4 for that.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    input_schema: dict[str, Any]
    permission: str
    risk: str  # "LOW" | "MEDIUM" | "HIGH" — see docs/07-agents/permissions.md
    confirmation_required: bool = False


@dataclass(frozen=True)
class ToolCall:
    """What the model proposed. This is a PROPOSAL only — see
    docs/07-agents/permissions.md "Non-negotiable rules": a tool call is
    never executed solely because the model produced it. Nothing in this
    class carries any authority; permission/risk/confirmation are decided
    by the backend against the real ToolDefinition, never by the model.
    """

    name: str
    arguments: dict[str, Any]


class ToolCallOutcome(str, Enum):
    """How a provider classified its own output when tools were offered.

    Part of the LLMProvider contract itself (any provider must be able to
    report these), not an Ollama-specific detail — see
    docs/adr/0012-tool-calling-contract.md for why this granularity exists:
    the audit trail must distinguish "no tool needed" from "the model tried
    and failed," which a plain content/tool_call split cannot express.
    """

    NO_TOOL_CALL = "no_tool_call"
    VALID = "valid"
    MALFORMED = "malformed"
    UNKNOWN_TOOL = "unknown_tool"
    INVALID_ARGUMENTS = "invalid_arguments"


@dataclass(frozen=True)
class LLMResponse:
    """Either a plain-text completion or a tool-call proposal, never both.

    `tool_call_outcome` is only meaningful when `tools` were offered to
    `generate()` — see `ToolCallOutcome` for what each value means for audit
    logging (docs/07-agents/audit.md).
    """

    content: str | None
    tool_call: ToolCall | None
    tool_call_outcome: ToolCallOutcome | None = None

    @property
    def is_tool_call(self) -> bool:
        return self.tool_call is not None
