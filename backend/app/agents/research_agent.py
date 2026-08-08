"""ResearchAgent — implements exactly docs/07-agents/agents/research-agent.md,
no more: retrieve + synthesize + attribute sources, session-scoped memory
only, no autonomous action beyond that.

Orchestration (docs/07-agents/agent-lifecycle.md, this Gate's mandatory
architecture):

    User request -> AIService -> LLMProvider -> tool proposal
        -> Tool Registry -> Permission validation -> Argument validation
        -> Tool execution -> AuditLog -> AI synthesis -> Response

The tool is never executed "because the model asked" — see
docs/adr/0012-tool-calling-contract.md and app/tools/pipeline.py.
"""
import uuid
from dataclasses import dataclass, field

from app.ai.service import AIService
from app.ai.types import ToolCallOutcome
from app.models.audit_log import AuditOutcome
from app.repositories.audit_log_repository import AuditLogRepository
from app.tools.pipeline import PipelineOutcome, authorize_tool_call
from app.tools.registry import ToolRegistry

AGENT_NAME = "research_agent"

# Phase 1: every authenticated caller implicitly has this scope — there is no
# per-user grant table yet (see docs/09-backend/authentication.md open
# decisions). This is a placeholder for *where permissions come from*, not a
# bypass of the check itself: authorize_tool_call() still runs for real on
# every call, against the tool's actual required permission.
GRANTED_PERMISSIONS = {"research.read"}

_SYSTEM_PROMPT = (
    "You are iNOVA's ResearchAgent. You have exactly one tool available: "
    "read_rss_feed, which only accepts a feed_id from the allowed list you are "
    "given — you can never supply a URL directly. Only propose a tool call if "
    "the user's request is clearly about reading one of the available feeds. "
    "For anything else, respond in plain text explaining you can only help "
    "with the feeds you have access to."
)

_TOOL_OUTCOME_TO_AUDIT = {
    ToolCallOutcome.MALFORMED: AuditOutcome.INVALID_TOOL_CALL,
    ToolCallOutcome.UNKNOWN_TOOL: AuditOutcome.INVALID_TOOL_CALL,
    ToolCallOutcome.INVALID_ARGUMENTS: AuditOutcome.INVALID_ARGUMENTS,
}

_PIPELINE_OUTCOME_TO_AUDIT = {
    PipelineOutcome.PERMISSION_DENIED: AuditOutcome.PERMISSION_DENIED,
    PipelineOutcome.CONFIRMATION_REQUIRED: AuditOutcome.CONFIRMATION_REQUIRED,
}

_USER_FACING_MESSAGE = {
    AuditOutcome.INVALID_TOOL_CALL: "I couldn't work out how to help with that using my available tools.",
    AuditOutcome.INVALID_ARGUMENTS: "I tried to use a tool for this, but the request was incomplete or invalid.",
    AuditOutcome.PERMISSION_DENIED: "You don't have permission to use this capability.",
    AuditOutcome.CONFIRMATION_REQUIRED: "This action requires confirmation before it can proceed.",
}


@dataclass(frozen=True)
class ResearchResult:
    answer: str
    sources: list[dict] = field(default_factory=list)
    audit_id: uuid.UUID | None = None
    outcome: str = AuditOutcome.SUCCESS.value


class ResearchAgent:
    def __init__(
        self,
        ai_service: AIService,
        tool_registry: ToolRegistry,
        audit_repo: AuditLogRepository,
        granted_permissions: set[str] | None = None,
    ):
        self._ai = ai_service
        self._registry = tool_registry
        self._audit = audit_repo
        # Overridable for tests only (e.g. proving the permission-denied path
        # end to end) — production call sites never pass this, see
        # docs/07-agents/agents/research-agent.md "Permissions".
        # NOTE: must check `is not None`, not truthiness — an intentionally
        # empty set() is falsy in Python and would silently fall back to the
        # default otherwise, defeating the permission-denied test case this
        # parameter exists for.
        self._granted_permissions = granted_permissions if granted_permissions is not None else GRANTED_PERMISSIONS

    def research(self, query: str, user_id: uuid.UUID, confirmed: bool = False) -> ResearchResult:
        tools = self._registry.definitions_for_permissions(self._granted_permissions)
        response = self._ai.generate(query, tools=tools, system=_SYSTEM_PROMPT)

        if not response.is_tool_call:
            if response.tool_call_outcome in _TOOL_OUTCOME_TO_AUDIT:
                audit_outcome = _TOOL_OUTCOME_TO_AUDIT[response.tool_call_outcome]
                entry = self._audit.record(
                    user_id=user_id,
                    agent_name=AGENT_NAME,
                    outcome=audit_outcome,
                    success=False,
                    result_summary=f"tool_call_outcome={response.tool_call_outcome.value}",
                )
                return ResearchResult(
                    answer=_USER_FACING_MESSAGE[audit_outcome], audit_id=entry.id, outcome=audit_outcome.value
                )
            # Genuine no-tool-needed completion — not a permissioned action,
            # nothing to audit (see docs/07-agents/audit.md scope: audits
            # cover permissioned/tool actions, not plain conversation).
            return ResearchResult(answer=response.content or "")

        tool_call = response.tool_call
        decision = authorize_tool_call(
            tool_call, registry=self._registry, granted_permissions=self._granted_permissions, confirmed=confirmed
        )

        if not decision.is_allowed:
            audit_outcome = _PIPELINE_OUTCOME_TO_AUDIT[decision.outcome]
            entry = self._audit.record(
                user_id=user_id,
                agent_name=AGENT_NAME,
                outcome=audit_outcome,
                success=False,
                tool_name=tool_call.name,
                permission=decision.registered_tool.definition.permission if decision.registered_tool else None,
                risk=decision.registered_tool.definition.risk if decision.registered_tool else None,
                result_summary=decision.reason,
            )
            return ResearchResult(
                answer=_USER_FACING_MESSAGE[audit_outcome], audit_id=entry.id, outcome=audit_outcome.value
            )

        registered = decision.registered_tool
        result = registered.handler(tool_call.arguments)

        if not result.success:
            entry = self._audit.record(
                user_id=user_id,
                agent_name=AGENT_NAME,
                outcome=AuditOutcome.EXECUTION_FAILED,
                success=False,
                tool_name=tool_call.name,
                permission=registered.definition.permission,
                risk=registered.definition.risk,
                result_summary=result.error,
            )
            return ResearchResult(
                answer=f"I attempted to fetch that, but it failed: {result.error}",
                audit_id=entry.id,
                outcome=AuditOutcome.EXECUTION_FAILED.value,
            )

        entry = self._audit.record(
            user_id=user_id,
            agent_name=AGENT_NAME,
            outcome=AuditOutcome.SUCCESS,
            success=True,
            tool_name=tool_call.name,
            permission=registered.definition.permission,
            risk=registered.definition.risk,
            result_summary=result.summary,
        )

        sources = (result.data or {}).get("items", [])
        answer = self._synthesize(query, result.summary, sources)
        return ResearchResult(answer=answer, sources=sources, audit_id=entry.id, outcome=AuditOutcome.SUCCESS.value)

    def _synthesize(self, query: str, tool_summary: str, sources: list[dict]) -> str:
        source_lines = "\n".join(f"- {s['title']} ({s['link']})" for s in sources if s.get("title"))
        prompt = (
            f"The user asked: {query}\n\n"
            f"You fetched this from an allowed RSS feed:\n{tool_summary}\n\n"
            f"Sources:\n{source_lines}\n\n"
            "Write a short, direct answer for the user based only on the above. "
            "Do not invent information beyond what was fetched."
        )
        response = self._ai.generate(prompt)
        return response.content or tool_summary
