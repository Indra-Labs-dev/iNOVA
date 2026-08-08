# iNOVA — Copyright (c) 2026 Archange Elie Yatte (AEY)
"""Application settings, loaded from environment variables.

See docs/09-backend/architecture.md and docs/12-security/secrets.md — no
secret ever has a real default here; .env.example documents the variables
with dummy placeholder values only.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_NAME = "iNOVA"
PROJECT_AUTHOR = "Archange Elie Yatte"
PROJECT_AUTHOR_ID = "AEY"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # General
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:8080"]

    # Database (see docs/10-data/postgresql.md)
    database_url: str = "postgresql+psycopg2://inova:inova_dev_password@localhost:5434/inova"

    # Auth (see docs/adr/0010-authentication-approach.md)
    jwt_secret_key: str = "CHANGE_ME_DEV_ONLY_NOT_A_REAL_SECRET"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    # AI / Ollama (see docs/06-ai/ollama.md, docs/adr/0005-ollama-local-llm.md addendum:
    # qwen2.5-coder:3b is the tag actually available in this environment; swap via
    # OLLAMA_MODEL env var, no code change needed, once qwen2.5:3b-instruct-q4_K_M
    # or another tag has been pulled)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-coder:3b"
    ollama_request_timeout_seconds: float = 60.0

    # Conversation memory (see docs/06-ai/context-management.md, docs/06-ai/memory.md
    # "MVP scope: short-term conversation memory only"). Bounded window of prior
    # messages included in each prompt. 20 chosen empirically via the Gate 4.4
    # experiment against real qwen2.5-coder:3b (see docs/06-ai/context-management.md
    # "Chosen window"): latency stayed flat (~0.5-2.3s) from 5 to 40 messages, but
    # recall of an earlier fact was 100% correct only when it fell inside the
    # window, and confidently wrong (not a hedge/decline) when it fell outside —
    # so a larger window is close to free and meaningfully safer here.
    conversation_history_window: int = 20


@lru_cache
def get_settings() -> Settings:
    return Settings()
