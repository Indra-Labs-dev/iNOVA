from fastapi import APIRouter

from app.core.config import PROJECT_NAME
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service=f"{PROJECT_NAME} API")
