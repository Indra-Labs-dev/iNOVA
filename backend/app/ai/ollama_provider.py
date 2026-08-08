"""Concrete LLMProvider backed by a local Ollama instance.

See docs/06-ai/ollama.md for the model/tag actually configured in this
environment, and docs/adr/0005-ollama-local-llm.md for the decision + its
2026-08-08 addendum explaining the tag substitution.

Tool-calling note (docs/adr/0012-tool-calling-contract.md): qwen2.5-coder:3b
never populates Ollama's native `message.tool_calls` field in practice — it
emits a tool-call proposal as JSON text in `message.content` (sometimes
markdown-fenced). This provider is the ONLY place that knows this — see
`app/ai/tool_call_parsing.py` for the text-parsing logic it delegates to.
"""
import httpx

from app.ai.provider import LLMProvider
from app.ai.tool_call_parsing import parse_tool_response
from app.ai.types import LLMResponse, ToolCallOutcome, ToolDefinition
from app.core.config import get_settings

settings = get_settings()


class OllamaError(Exception):
    """Raised when Ollama is unreachable or returns an unexpected response."""


def _to_ollama_tool(tool: ToolDefinition) -> dict:
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.input_schema,
        },
    }


class OllamaProvider(LLMProvider):
    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout_seconds: float | None = None,
    ):
        self._base_url = base_url or settings.ollama_base_url
        self._model = model or settings.ollama_model
        self._timeout = timeout_seconds or settings.ollama_request_timeout_seconds

    def generate(
        self,
        message: str,
        tools: list[ToolDefinition] | None = None,
        system: str | None = None,
        history: list[dict[str, str]] | None = None,
    ) -> LLMResponse:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": message})

        payload = {"model": self._model, "messages": messages, "stream": False}
        if tools:
            payload["tools"] = [_to_ollama_tool(t) for t in tools]

        try:
            response = httpx.post(
                f"{self._base_url}/api/chat",
                json=payload,
                timeout=self._timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OllamaError(f"Ollama request failed: {exc}") from exc

        data = response.json()
        try:
            raw_content = data["message"]["content"]
        except (KeyError, TypeError) as exc:
            raise OllamaError(f"Unexpected Ollama response shape: {data}") from exc

        if not tools:
            return LLMResponse(content=raw_content, tool_call=None)

        parsed = parse_tool_response(raw_content, tools)
        if parsed.outcome == ToolCallOutcome.VALID:
            return LLMResponse(content=None, tool_call=parsed.tool_call, tool_call_outcome=parsed.outcome)
        # Anything not cleanly VALID (malformed/unknown tool/invalid args/no
        # tool call) still surfaces as plain content for a caller that only
        # wants text — but `tool_call_outcome` is preserved so a caller that
        # cares (ResearchAgent, for audit purposes) can tell "the model
        # tried and failed" apart from "the model genuinely didn't need a
        # tool" — see docs/adr/0012 and docs/07-agents/audit.md.
        return LLMResponse(content=raw_content, tool_call=None, tool_call_outcome=parsed.outcome)

    @property
    def model(self) -> str:
        return self._model
