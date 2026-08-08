"""API-layer tests for POST /api/v1/missions.

Mirrors tests/test_agents_api.py's pattern (real register/login flow,
scripted LLMProvider, respx-mocked RSS feed). The security-critical cases
here are specific to Gate 3: MissionRequest has no field for user_id,
xp_awarded, permission, risk, or agent_name, so a client that sends them
anyway must have zero effect — the persisted mission must always belong to
the authenticated caller and carry only server-computed XP.
"""
import uuid

import httpx
import respx

from app.ai.provider import LLMProvider
from app.ai.types import LLMResponse, ToolCall, ToolCallOutcome
from app.api.deps import get_llm_provider
from app.main import app
from app.repositories.mission_repository import MissionRepository
from app.repositories.user_repository import UserRepository
from app.tools.research_tools import RSS_ALLOWLIST

VALID_RSS = b"""<?xml version="1.0"?>
<rss version="2.0"><channel><title>Python Insider</title>
<item><title>Python 3.14 released</title><link>https://blog.python.org/1</link><pubDate>Mon, 01 Jan 2026 00:00:00 GMT</pubDate></item>
</channel></rss>"""


class ScriptedLLM(LLMProvider):
    model = "scripted-llm"

    def __init__(self, responses):
        self._responses = list(responses)

    def generate(self, message, tools=None, system=None):
        return self._responses.pop(0)


def _register_and_login(client, email="mission-runner@inova.dev"):
    client.post("/api/v1/auth/register", json={"email": email, "password": "correct-horse-battery"})
    tokens = client.post("/api/v1/auth/login", json={"email": email, "password": "correct-horse-battery"}).json()
    return tokens["access_token"]


def _success_scripted_llm():
    return ScriptedLLM(
        [
            LLMResponse(
                content=None,
                tool_call=ToolCall(name="read_rss_feed", arguments={"feed_id": "python_blog"}),
                tool_call_outcome=ToolCallOutcome.VALID,
            ),
            LLMResponse(content="Python 3.14 was just released.", tool_call=None),
        ]
    )


def test_create_mission_requires_authentication(client):
    response = client.post("/api/v1/missions", json={"goal": "What's new for Python?"})
    assert response.status_code == 401


@respx.mock
def test_create_mission_returns_answer_sources_and_xp_when_authenticated(client):
    access_token = _register_and_login(client)
    respx.get(RSS_ALLOWLIST["python_blog"]).mock(return_value=httpx.Response(200, content=VALID_RSS))

    app.dependency_overrides[get_llm_provider] = lambda: _success_scripted_llm()
    try:
        response = client.post(
            "/api/v1/missions",
            json={"goal": "What's new for Python?"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
    finally:
        del app.dependency_overrides[get_llm_provider]

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "completed"
    assert body["answer"] == "Python 3.14 was just released."
    assert body["sources"][0]["title"] == "Python 3.14 released"
    assert body["xp_awarded"] == 10
    assert body["failure_reason"] is None


def test_create_mission_rejects_empty_goal(client):
    access_token = _register_and_login(client, email="empty-goal@inova.dev")
    response = client.post(
        "/api/v1/missions", json={"goal": ""}, headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 422


@respx.mock
def test_client_supplied_authority_fields_are_ignored(client, db_session):
    """Regression test for the Gate 3 GO requirement: user_id, xp_awarded,
    permission, risk, and agent_name must never be accepted from the client
    as authoritative values, even if a client sends them.
    """
    access_token = _register_and_login(client, email="attacker@inova.dev")
    respx.get(RSS_ALLOWLIST["python_blog"]).mock(return_value=httpx.Response(200, content=VALID_RSS))

    other_user_id = str(uuid.uuid4())
    app.dependency_overrides[get_llm_provider] = lambda: _success_scripted_llm()
    try:
        response = client.post(
            "/api/v1/missions",
            json={
                "goal": "What's new for Python?",
                "user_id": other_user_id,
                "xp_awarded": 999999,
                "permission": "admin.all",
                "risk": "none",
                "agent_name": "totally_not_research_agent",
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
    finally:
        del app.dependency_overrides[get_llm_provider]

    assert response.status_code == 201
    body = response.json()
    # Server-computed XP, not the client-supplied 999999.
    assert body["xp_awarded"] == 10

    actual_user = UserRepository(db_session).get_by_email("attacker@inova.dev")
    mission = MissionRepository(db_session).get_by_id(uuid.UUID(body["id"]))
    # Mission belongs to the authenticated caller, not the spoofed user_id.
    assert mission.user_id == actual_user.id
    assert str(mission.user_id) != other_user_id
    assert mission.agent_name == "research_agent"
    assert mission.xp_awarded == 10
