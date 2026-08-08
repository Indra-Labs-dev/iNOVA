"""Shared types for the LLMProvider tool-calling contract.

See docs/06-ai/llm-provider.md (`generate(messages, tools?) -> completion |
tool_call`) and docs/07-agents/tools.md for the tool definition shape.
Gate 1 scope (docs/adr/0012-tool-calling-contract.md): only the fields
needed to prove the contract end to end. `permission`/`risk`/`confirmation`
are carried on `ToolDefinition` per docs/07-agents/permissions.md, but no
permission *system* (registry storage, grants) is built yet — see
docs/16-roadmap/phases.md Phase 4 for that.
"""
from dataclasses import dataclass
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


@dataclass(frozen=True)
class LLMResponse:
    """Either a plain-text completion or a tool-call proposal, never both."""

    content: str | None
    tool_call: ToolCall | None

    @property
    def is_tool_call(self) -> bool:
        return self.tool_call is not None
