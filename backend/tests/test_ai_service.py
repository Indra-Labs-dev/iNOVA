from app.ai.provider import LLMProvider
from app.ai.service import AIService
from app.ai.types import LLMResponse, ToolCall, ToolDefinition


class StubProvider(LLMProvider):
    model = "stub-model"

    def __init__(self, response: LLMResponse | None = None):
        self.last_message = None
        self.last_tools = None
        self.last_system = None
        self._response = response or LLMResponse(content="stubbed response", tool_call=None)

    def generate(self, message: str, tools=None, system=None) -> LLMResponse:
        self.last_message = message
        self.last_tools = tools
        self.last_system = system
        return self._response


def test_ai_service_chat_delegates_to_provider():
    provider = StubProvider()
    service = AIService(provider)

    result = service.chat("hello")

    assert result == "stubbed response"
    assert provider.last_message == "hello"
    assert provider.last_tools is None


def test_ai_service_generate_passes_tools_through():
    tool = ToolDefinition(
        name="read_rss_feed",
        description="Fetch an RSS feed.",
        input_schema={"type": "object", "properties": {"feed": {"type": "string"}}, "required": ["feed"]},
        permission="research.read",
        risk="LOW",
    )
    provider = StubProvider(LLMResponse(content=None, tool_call=ToolCall(name="read_rss_feed", arguments={"feed": "https://example.com/feed.xml"})))
    service = AIService(provider)

    response = service.generate("give me the feed", tools=[tool])

    assert provider.last_tools == [tool]
    assert response.is_tool_call
    assert response.tool_call.name == "read_rss_feed"


def test_ai_service_chat_handles_tool_call_response_gracefully():
    # chat() is the no-tools convenience path; if a provider somehow returns
    # a tool_call with no content, chat() must not crash — it degrades to "".
    provider = StubProvider(LLMResponse(content=None, tool_call=ToolCall(name="x", arguments={})))
    service = AIService(provider)

    assert service.chat("hello") == ""


def test_ai_service_exposes_model_name():
    service = AIService(StubProvider())
    assert service.model_name == "stub-model"


def test_ai_service_only_depends_on_llm_provider_interface():
    # Regression guard for docs/adr/0006-llmprovider-abstraction.md: AIService
    # must be constructible with *any* LLMProvider, not just OllamaProvider.
    assert AIService.__init__.__annotations__["provider"] is LLMProvider
