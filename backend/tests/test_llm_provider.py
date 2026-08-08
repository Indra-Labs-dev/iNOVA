"""OllamaProvider tests — HTTP mocked via respx, no real Ollama/GPU needed
(see docs/14-testing/agent-tests.md)."""
import httpx
import pytest
import respx

from app.ai.ollama_provider import OllamaError, OllamaProvider


@respx.mock
def test_generate_returns_message_content():
    respx.post("http://fake-ollama:11434/api/chat").mock(
        return_value=httpx.Response(200, json={"message": {"content": "hi there"}})
    )
    provider = OllamaProvider(base_url="http://fake-ollama:11434", model="test-model")

    result = provider.generate("hello")

    assert result == "hi there"


@respx.mock
def test_generate_raises_on_http_error():
    respx.post("http://fake-ollama:11434/api/chat").mock(return_value=httpx.Response(500))
    provider = OllamaProvider(base_url="http://fake-ollama:11434", model="test-model")

    with pytest.raises(OllamaError):
        provider.generate("hello")


@respx.mock
def test_generate_raises_on_unexpected_response_shape():
    respx.post("http://fake-ollama:11434/api/chat").mock(return_value=httpx.Response(200, json={"unexpected": True}))
    provider = OllamaProvider(base_url="http://fake-ollama:11434", model="test-model")

    with pytest.raises(OllamaError):
        provider.generate("hello")
