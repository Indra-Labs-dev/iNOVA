"""Mission endpoints — see docs/08-modules/mission-system.md and
docs/09-backend/api-design.md.

Thin router: all orchestration lives in MissionService (see
docs/09-backend/architecture.md layer rules). `current_user` is resolved
server-side from the JWT — the request body carries only `goal`, never a
user_id, xp_awarded, permission, risk, or agent_name (see
app/schemas/missions.py: there is no field for any of those to land in).
"""
from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_mission_service
from app.models.user import User
from app.schemas.missions import MissionRequest, MissionResponse
from app.services.mission_service import MissionService

router = APIRouter()


@router.post("", response_model=MissionResponse, status_code=201)
def create_mission(
    payload: MissionRequest,
    current_user: User = Depends(get_current_user),
    service: MissionService = Depends(get_mission_service),
) -> MissionResponse:
    outcome = service.start(payload.goal, user_id=current_user.id)
    mission = outcome.mission
    return MissionResponse(
        id=str(mission.id),
        status=mission.status,
        answer=mission.answer or "",
        sources=outcome.sources,
        xp_awarded=mission.xp_awarded,
        failure_reason=mission.failure_reason,
    )
