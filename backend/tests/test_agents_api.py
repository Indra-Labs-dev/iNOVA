"""API-layer tests for POST /api/v1/agents/research.

Auth path uses the real register/login flow (SQLite, see conftest.py).
Tool-call behavior uses a scripted LLMProvider override, same pattern as
test_research_agent.py, to prove the pipeline works through the actual
HTTP layer, not just at the service layer.
"""
import httpx
import respx

from app.ai.provider import LLMProvider
from app.ai.types import LLMResponse, ToolCall, ToolCallOutcome
from app.api.deps import get_llm_provider
from app.main import app
from app.tools.research_tools import RSS_ALLOWLIST

VALID_RSS = b"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>Python Insider</title>
<item><title>Python 3.14 released</title><link>https://blog.python.org/1</link><pubDate>Mon, 01 Jan 2026 00:00:00 GMT</pubDate></item>
</channel></rss>"""


class ScriptedLLM(LLMProvider):
    model = "scripted-llm"

    def __init__(self, responses):
        self._responses = list(responses)

    def generate(self, message, tools=None, system=None, history=None):
        return self._responses.pop(0)


def _register_and_login(client, email="researcher@inova.dev"):
    client.post("/api/v1/auth/register", json={"email": email, "password": "correct-horse-battery"})
    tokens = client.post("/api/v1/auth/login", json={"email": email, "password": "correct-horse-battery"}).json()
    return tokens["access_token"]


def test_research_requires_authentication(client):
    response = client.post("/api/v1/agents/research", json={"query": "test"})
    assert response.status_code == 401


@respx.mock
def test_research_returns_answer_and_sources_when_authenticated(client):
    access_token = _register_and_login(client)
    respx.get(RSS_ALLOWLIST["python_blog"]).mock(return_value=httpx.Response(200, content=VALID_RSS))

    scripted = ScriptedLLM(
        [
            LLMResponse(
                content=None,
                tool_call=ToolCall(name="read_rss_feed", arguments={"feed_id": "python_blog"}),
                tool_call_outcome=ToolCallOutcome.VALID,
            ),
            LLMResponse(content="Python 3.14 was just released.", tool_call=None),
        ]
    )
    app.dependency_overrides[get_llm_provider] = lambda: scripted
    try:
        response = client.post(
            "/api/v1/agents/research",
            json={"query": "What's new for Python?"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
    finally:
        del app.dependency_overrides[get_llm_provider]

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "Python 3.14 was just released."
    assert body["outcome"] == "success"
    assert body["sources"][0]["title"] == "Python 3.14 released"
    assert body["audit_id"] is not None


def test_research_rejects_empty_query(client):
    access_token = _register_and_login(client, email="empty-query@inova.dev")
    response = client.post(
        "/api/v1/agents/research", json={"query": ""}, headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 422
