"""Backend-owned Tool Registry — see docs/07-agents/tools.md and
docs/adr/0013-static-tool-registry.md.

Static, in-code, populated once at import time (see app/tools/research_tools.py
for the real tools registered into `default_registry`). No API endpoint can
register, modify, or remove a tool, its permission, or its risk level — the
registry is a Python object, never a database row a request could reach.
"""
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from app.ai.types import ToolDefinition


@dataclass(frozen=True)
class ToolExecutionResult:
    """What a tool handler returns after actually running.

    `summary` is what gets audited and handed back to the LLM for synthesis —
    keep it bounded and free of sensitive detail (see docs/12-security/secrets.md).
    `data` is optional structured output for the API response (e.g. item list).
    """

    success: bool
    summary: str
    data: dict[str, Any] | None = None
    error: str | None = None


ToolHandler = Callable[[dict[str, Any]], ToolExecutionResult]


@dataclass(frozen=True)
class RegisteredTool:
    definition: ToolDefinition
    handler: ToolHandler


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool] = {}

    def register(self, tool: RegisteredTool) -> None:
        if tool.definition.name in self._tools:
            raise ValueError(f"Tool '{tool.definition.name}' is already registered")
        self._tools[tool.definition.name] = tool

    def get(self, name: str) -> RegisteredTool | None:
        return self._tools.get(name)

    def definitions_for_permissions(self, granted_permissions: set[str]) -> list[ToolDefinition]:
        """Only the tools the caller's permissions cover — see docs/07-agents/tools.md
        'Allowlisting': no agent sees the full registry regardless of caller."""
        return [
            t.definition
            for t in self._tools.values()
            if t.definition.permission in granted_permissions
        ]

    def all_definitions(self) -> list[ToolDefinition]:
        return [t.definition for t in self._tools.values()]


# Process-wide singleton populated at import time by app/tools/research_tools.py
# (and any future tool module) — see docs/adr/0013-static-tool-registry.md.
default_registry = ToolRegistry()
