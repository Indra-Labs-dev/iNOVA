"""Concrete LLMProvider backed by a local Ollama instance.

See docs/06-ai/ollama.md for the model/tag actually configured in this
environment, and docs/adr/0005-ollama-local-llm.md for the decision + its
2026-08-08 addendum explaining the tag substitution.
"""
import httpx

from app.ai.provider import LLMProvider
from app.core.config import get_settings

settings = get_settings()


class OllamaError(Exception):
    """Raised when Ollama is unreachable or returns an unexpected response."""


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

    def generate(self, message: str) -> str:
        try:
            response = httpx.post(
                f"{self._base_url}/api/chat",
                json={
                    "model": self._model,
                    "messages": [{"role": "user", "content": message}],
                    "stream": False,
                },
                timeout=self._timeout,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise OllamaError(f"Ollama request failed: {exc}") from exc

        data = response.json()
        try:
            return data["message"]["content"]
        except (KeyError, TypeError) as exc:
            raise OllamaError(f"Unexpected Ollama response shape: {data}") from exc

    @property
    def model(self) -> str:
        return self._model
