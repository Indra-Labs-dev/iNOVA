from fastapi import APIRouter

from app.api.v1.agents import router as agents_router
from app.api.v1.ai import router as ai_router
from app.api.v1.auth import router as auth_router
from app.api.v1.conversations import router as conversations_router
from app.api.v1.health import router as health_router
from app.api.v1.missions import router as missions_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(ai_router, prefix="/ai", tags=["ai"])
api_router.include_router(agents_router, prefix="/agents", tags=["agents"])
api_router.include_router(missions_router, prefix="/missions", tags=["missions"])
api_router.include_router(conversations_router, prefix="/conversations", tags=["conversations"])
