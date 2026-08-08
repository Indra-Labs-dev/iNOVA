from app.ai.provider import LLMProvider
from app.ai.service import AIService


class StubProvider(LLMProvider):
    model = "stub-model"

    def __init__(self):
        self.last_message = None

    def generate(self, message: str) -> str:
        self.last_message = message
        return "stubbed response"


def test_ai_service_delegates_to_provider():
    provider = StubProvider()
    service = AIService(provider)

    result = service.chat("hello")

    assert result == "stubbed response"
    assert provider.last_message == "hello"


def test_ai_service_exposes_model_name():
    service = AIService(StubProvider())
    assert service.model_name == "stub-model"


def test_ai_service_only_depends_on_llm_provider_interface():
    # Regression guard for docs/adr/0006-llmprovider-abstraction.md: AIService
    # must be constructible with *any* LLMProvider, not just OllamaProvider.
    assert AIService.__init__.__annotations__["provider"] is LLMProvider
