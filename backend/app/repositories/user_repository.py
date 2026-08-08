"""Data access for User/Session — kept separate from business logic
(see docs/09-backend/architecture.md layer rules)."""
import uuid
from datetime import datetime

from sqlalchemy.orm import Session as DbSession

from app.models.session import Session
from app.models.user import User


class UserRepository:
    def __init__(self, db: DbSession):
        self._db = db

    def get_by_email(self, email: str) -> User | None:
        return self._db.query(User).filter(User.email == email).one_or_none()

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self._db.query(User).filter(User.id == user_id).one_or_none()

    def create(self, email: str, password_hash: str) -> User:
        user = User(email=email, password_hash=password_hash)
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def create_session(self, user_id: uuid.UUID, refresh_token_hash: str, expires_at: datetime) -> Session:
        session = Session(user_id=user_id, refresh_token_hash=refresh_token_hash, expires_at=expires_at)
        self._db.add(session)
        self._db.commit()
        self._db.refresh(session)
        return session

    def get_active_sessions_for_user(self, user_id: uuid.UUID) -> list[Session]:
        return (
            self._db.query(Session)
            .filter(Session.user_id == user_id, Session.revoked_at.is_(None))
            .all()
        )

    def get_active_session_by_refresh_hash(self, refresh_token_hash: str) -> Session | None:
        return (
            self._db.query(Session)
            .filter(Session.refresh_token_hash == refresh_token_hash, Session.revoked_at.is_(None))
            .one_or_none()
        )

    def revoke_session(self, session: Session, revoked_at: datetime) -> None:
        session.revoked_at = revoked_at
        self._db.commit()
