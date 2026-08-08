"""Data access for UserProgress (XP) — see docs/08-modules/gamification.md.

`add_xp` is the only write path — there is no method to set XP to an
arbitrary value, by design: XP can only ever be incremented by server-side
logic (MissionService), never set directly from a request.
"""
import uuid

from sqlalchemy.orm import Session as DbSession

from app.models.user_progress import UserProgress


class UserProgressRepository:
    def __init__(self, db: DbSession):
        self._db = db

    def get(self, user_id: uuid.UUID) -> UserProgress | None:
        return self._db.query(UserProgress).filter(UserProgress.user_id == user_id).one_or_none()

    def add_xp(self, user_id: uuid.UUID, amount: int) -> UserProgress:
        if amount < 0:
            raise ValueError("add_xp does not accept negative amounts — XP never decreases here.")

        progress = self.get(user_id)
        if progress is None:
            progress = UserProgress(user_id=user_id, xp=amount)
            self._db.add(progress)
        else:
            progress.xp += amount
        self._db.commit()
        self._db.refresh(progress)
        return progress
