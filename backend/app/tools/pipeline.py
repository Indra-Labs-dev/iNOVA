"""Backend authorization pipeline for a tool-call proposal — see
docs/07-agents/permissions.md and this Gate's mandatory architecture:

    LLM -> Tool proposal -> Backend validation -> Tool Registry
        -> Permission Check -> Risk Check -> Confirmation Gate -> Execution

`parse_tool_response` (app/ai/tool_call_parsing.py) already covers "does the
tool exist" and "is the schema valid" (as part of parsing, since both need
the offered-tools list). This module covers what comes after a VALID parse:
permission and confirmation — the two things the LLM must NEVER get to
decide for itself (see docs/adr/0012-tool-calling-contract.md).
"""
from dataclasses import dataclass
from enum import Enum

from app.ai.types import ToolCall
from app.tools.registry import RegisteredTool, ToolRegistry


class PipelineOutcome(str, Enum):
    ALLOWED = "allowed"
    PERMISSION_DENIED = "permission_denied"
    CONFIRMATION_REQUIRED = "confirmation_required"


@dataclass(frozen=True)
class PipelineDecision:
    outcome: PipelineOutcome
    registered_tool: RegisteredTool | None
    reason: str | None = None

    @property
    def is_allowed(self) -> bool:
        return self.outcome == PipelineOutcome.ALLOWED


def authorize_tool_call(
    tool_call: ToolCall,
    registry: ToolRegistry,
    granted_permissions: set[str],
    confirmed: bool = False,
) -> PipelineDecision:
    """Never trusts anything on `tool_call` beyond its name/arguments shape —
    permission, risk, and confirmation requirements are read exclusively from
    the registry's ToolDefinition, never from the model's proposal."""
    registered = registry.get(tool_call.name)
    if registered is None:
        # Should not happen if tool_call came from a VALID parse against this
        # same registry, but never assume that invariant holds — defense in
        # depth per docs/06-ai/tool-use.md.
        return PipelineDecision(
            PipelineOutcome.PERMISSION_DENIED, None, reason=f"'{tool_call.name}' is not a registered tool"
        )

    required_permission = registered.definition.permission
    if required_permission not in granted_permissions:
        return PipelineDecision(
            PipelineOutcome.PERMISSION_DENIED,
            registered,
            reason=f"caller lacks required permission '{required_permission}'",
        )

    if registered.definition.confirmation_required and not confirmed:
        return PipelineDecision(
            PipelineOutcome.CONFIRMATION_REQUIRED,
            registered,
            reason=f"tool '{tool_call.name}' (risk={registered.definition.risk}) requires confirmation",
        )

    return PipelineDecision(PipelineOutcome.ALLOWED, registered)
