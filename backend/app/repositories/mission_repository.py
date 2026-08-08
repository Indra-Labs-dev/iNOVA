"""Data access for Mission — see docs/08-modules/mission-system.md.

No orchestration logic here — MissionService decides status/xp/outcome
mapping; this only persists it (see docs/09-backend/architecture.md layer
rules).
"""
import uuid
from datetime import datetime

from sqlalchemy.orm import Session as DbSession

from app.models.mission import Mission


class MissionRepository:
    def __init__(self, db: DbSession):
        self._db = db

    def create(
        self,
        *,
        user_id: uuid.UUID,
        goal: str,
        agent_name: str,
        status: str,
        answer: str | None,
        xp_awarded: int,
        failure_reason: str | None,
        audit_id: uuid.UUID | None,
        completed_at: datetime | None,
    ) -> Mission:
        mission = Mission(
            user_id=user_id,
            goal=goal,
            agent_name=agent_name,
            status=status,
            answer=answer,
            xp_awarded=xp_awarded,
            failure_reason=failure_reason,
            audit_id=audit_id,
            completed_at=completed_at,
        )
        self._db.add(mission)
        self._db.commit()
        self._db.refresh(mission)
        return mission

    def get_by_id(self, mission_id: uuid.UUID) -> Mission | None:
        return self._db.query(Mission).filter(Mission.id == mission_id).one_or_none()

    def list_for_user(self, user_id: uuid.UUID, limit: int = 50) -> list[Mission]:
        return (
            self._db.query(Mission)
            .filter(Mission.user_id == user_id)
            .order_by(Mission.created_at.desc())
            .limit(limit)
            .all()
        )
