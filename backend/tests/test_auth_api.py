"""End-to-end auth flow against the API layer (SQLite-backed, see conftest.py).

Covers docs/adr/0010-authentication-approach.md's register/login/refresh/logout
contract and the permission boundary on /auth/me.
"""


def test_register_then_login(client):
    register_response = client.post(
        "/api/v1/auth/register", json={"email": "aey@inova.dev", "password": "correct-horse-battery"}
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login", json={"email": "aey@inova.dev", "password": "correct-horse-battery"}
    )
    assert login_response.status_code == 200
    body = login_response.json()
    assert "access_token" in body
    assert "refresh_token" in body


def test_register_duplicate_email_rejected(client):
    payload = {"email": "dupe@inova.dev", "password": "correct-horse-battery"}
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "email_already_registered"


def test_login_wrong_password_rejected(client):
    client.post("/api/v1/auth/register", json={"email": "wrong@inova.dev", "password": "correct-horse-battery"})
    response = client.post("/api/v1/auth/login", json={"email": "wrong@inova.dev", "password": "not-the-password"})
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_credentials"


def test_me_requires_valid_token(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_me_returns_current_user_with_valid_token(client):
    client.post("/api/v1/auth/register", json={"email": "me@inova.dev", "password": "correct-horse-battery"})
    tokens = client.post(
        "/api/v1/auth/login", json={"email": "me@inova.dev", "password": "correct-horse-battery"}
    ).json()

    response = client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "me@inova.dev"


def test_refresh_rotates_token_and_invalidates_old_one(client):
    client.post("/api/v1/auth/register", json={"email": "refresh@inova.dev", "password": "correct-horse-battery"})
    tokens = client.post(
        "/api/v1/auth/login", json={"email": "refresh@inova.dev", "password": "correct-horse-battery"}
    ).json()

    refreshed = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert refreshed.status_code == 200
    assert refreshed.json()["refresh_token"] != tokens["refresh_token"]

    # Reusing the old (now-revoked) refresh token must fail — rotation-on-use.
    reused = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert reused.status_code == 401


def test_logout_revokes_refresh_token(client):
    client.post("/api/v1/auth/register", json={"email": "logout@inova.dev", "password": "correct-horse-battery"})
    tokens = client.post(
        "/api/v1/auth/login", json={"email": "logout@inova.dev", "password": "correct-horse-battery"}
    ).json()

    logout_response = client.post("/api/v1/auth/logout", json={"refresh_token": tokens["refresh_token"]})
    assert logout_response.status_code == 204

    reused = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert reused.status_code == 401
