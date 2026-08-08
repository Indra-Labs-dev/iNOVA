"""Proves the API-layer chat endpoint works end to end against a fake
provider (see conftest.py) — no real Ollama call in this test, per
docs/14-testing/agent-tests.md."""


def test_chat_returns_provider_response(client):
    response = client.post("/api/v1/ai/chat", json={"message": "hello iNOVA"})

    assert response.status_code == 200
    body = response.json()
    assert body["response"] == "echo: hello iNOVA"
    assert body["model"] == "fake-model"


def test_chat_rejects_empty_message(client):
    response = client.post("/api/v1/ai/chat", json={"message": ""})
    assert response.status_code == 422
    # Validation errors go through the same envelope as every other error —
    # see docs/09-backend/error-handling.md.
    assert response.json()["error"]["code"] == "validation_error"
