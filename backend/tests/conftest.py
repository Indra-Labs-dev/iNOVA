"""Shared test fixtures.

Uses an in-memory SQLite DB for API tests instead of requiring a running
Postgres — see docs/14-testing/strategy.md and docs/14-testing/api-tests.md.
Ollama is never called in tests; the LLMProvider dependency is overridden
with a fake (see docs/14-testing/agent-tests.md: don't depend on a heavy
local model in tests when a mock suffices).
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.ai.provider import LLMProvider
from app.ai.types import LLMResponse
from app.api.deps import get_db, get_llm_provider
from app.core.database import Base
from app.main import app


class FakeLLMProvider(LLMProvider):
    """Deterministic stand-in for OllamaProvider — no network, no GPU."""

    model = "fake-model"

    def generate(self, message: str, tools=None) -> LLMResponse:
        return LLMResponse(content=f"echo: {message}", tool_call=None)


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    def _get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override
    app.dependency_overrides[get_llm_provider] = lambda: FakeLLMProvider()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
