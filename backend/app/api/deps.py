"""FastAPI dependency wiring — the seam where routes get repositories/services.

Kept centralized so routes never construct these objects themselves (see
docs/09-backend/architecture.md layer rules).
"""
import uuid

import jwt
from fastapi import Depends, Header
from sqlalchemy.orm import Session as DbSession

from app.agents.research_agent import ResearchAgent
from app.ai.ollama_provider import OllamaProvider
from app.ai.provider import LLMProvider
from app.ai.service import AIService
from app.core.database import get_db
from app.core.errors import APIError
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.mission_repository import MissionRepository
from app.repositories.user_progress_repository import UserProgressRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.mission_service import MissionService
from app.tools.registry import ToolRegistry, default_registry

# Ensure built-in tools are registered before anything resolves the registry —
# importing the module is what triggers app/tools/research_tools.py's
# `default_registry.register(...)` call at import time (see
# docs/adr/0013-static-tool-registry.md).
import app.tools.research_tools  # noqa: F401,E402


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


def get_audit_log_repository(db: DbSession = Depends(get_db)) -> AuditLogRepository:
    return AuditLogRepository(db)


def get_tool_registry() -> ToolRegistry:
    return default_registry


def get_research_agent(
    ai_service: AIService = Depends(get_ai_service),
    tool_registry: ToolRegistry = Depends(get_tool_registry),
    audit_repo: AuditLogRepository = Depends(get_audit_log_repository),
) -> ResearchAgent:
    return ResearchAgent(ai_service, tool_registry, audit_repo)


def get_mission_repository(db: DbSession = Depends(get_db)) -> MissionRepository:
    return MissionRepository(db)


def get_user_progress_repository(db: DbSession = Depends(get_db)) -> UserProgressRepository:
    return UserProgressRepository(db)


def get_mission_service(
    research_agent: ResearchAgent = Depends(get_research_agent),
    mission_repo: MissionRepository = Depends(get_mission_repository),
    user_progress_repo: UserProgressRepository = Depends(get_user_progress_repository),
) -> MissionService:
    return MissionService(research_agent, mission_repo, user_progress_repo)
