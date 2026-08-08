"""FastAPI dependency wiring — the seam where routes get repositories/services.

Kept centralized so routes never construct these objects themselves (see
docs/09-backend/architecture.md layer rules).
"""
import uuid

import jwt
from fastapi import Depends, Header
from sqlalchemy.orm import Session as DbSession

from app.ai.ollama_provider import OllamaProvider
from app.ai.provider import LLMProvider
from app.ai.service import AIService
from app.core.database import get_db
from app.core.errors import APIError
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def get_user_repository(db: DbSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_auth_service(repository: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repository)


def get_llm_provider() -> LLMProvider:
    return OllamaProvider()


def get_ai_service(provider: LLMProvider = Depends(get_llm_provider)) -> AIService:
    return AIService(provider)


def get_current_user(
    authorization: str | None = Header(default=None),
    repository: UserRepository = Depends(get_user_repository),
) -> User:
    """Minimal bearer-token dependency for Phase 0.

    NOTE: `OAuth2PasswordBearer` (with its automatic OpenAPI "Authorize" button)
    would be the idiomatic upgrade once more than one protected route exists —
    a plain `Header` dependency is enough for the single `/auth/me` caller here,
    to avoid over-abstracting for one consumer.
    """
    if authorization is None or not authorization.startswith("Bearer "):
        raise APIError(401, "not_authenticated", "Missing or malformed Authorization header.")
    token = authorization.removeprefix("Bearer ")
    try:
        payload = decode_access_token(token)
        user_id = uuid.UUID(payload["sub"])
    except (jwt.PyJWTError, ValueError, KeyError) as exc:
        raise APIError(401, "invalid_token", "Invalid or expired access token.") from exc

    user = repository.get_by_id(user_id)
    if user is None or not user.is_active:
        raise APIError(401, "invalid_token", "Invalid or expired access token.")
    return user
