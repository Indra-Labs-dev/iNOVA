"""Authentication business logic — see docs/adr/0010-authentication-approach.md.

Phase 0 scope only: register, login, refresh. Email verification and MFA are
[PLANNED], not implemented here (see docs/09-backend/authentication.md).
"""
from datetime import datetime, timedelta, timezone

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository

settings = get_settings()


class AuthError(Exception):
    """Raised for any auth failure the API layer should turn into a 4xx response."""


def _as_aware_utc(value: datetime) -> datetime:
    """SQLite (used in tests, see tests/conftest.py) doesn't round-trip tzinfo on
    DateTime columns the way Postgres does — normalize defensively so refresh-token
    expiry comparisons work identically on both backends."""
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


class AuthService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    def register(self, email: str, password: str) -> User:
        if self._repository.get_by_email(email) is not None:
            raise AuthError("An account with this email already exists.")
        return self._repository.create(email=email, password_hash=hash_password(password))

    def login(self, email: str, password: str) -> tuple[str, str]:
        user = self._repository.get_by_email(email)
        if user is None or not user.is_active or not verify_password(password, user.password_hash):
            raise AuthError("Invalid email or password.")
        return self._issue_tokens(user)

    def refresh(self, refresh_token: str) -> tuple[str, str]:
        """Rotates the refresh token on every use: the old session is revoked and a
        new one issued, so a stolen-then-reused token is detectable (reuse of a
        revoked token) — see docs/12-security/authentication.md "revocable sessions"."""
        session = self._repository.get_active_session_by_refresh_hash(hash_refresh_token(refresh_token))
        if session is None or _as_aware_utc(session.expires_at) < datetime.now(timezone.utc):
            raise AuthError("Invalid or expired refresh token.")
        user = self._repository.get_by_id(session.user_id)
        if user is None or not user.is_active:
            raise AuthError("Invalid or expired refresh token.")
        self._repository.revoke_session(session, revoked_at=datetime.now(timezone.utc))
        return self._issue_tokens(user)

    def logout(self, refresh_token: str) -> None:
        session = self._repository.get_active_session_by_refresh_hash(hash_refresh_token(refresh_token))
        if session is not None:
            self._repository.revoke_session(session, revoked_at=datetime.now(timezone.utc))

    def _issue_tokens(self, user: User) -> tuple[str, str]:
        access_token = create_access_token(subject=str(user.id))
        refresh_token = generate_refresh_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
        self._repository.create_session(
            user_id=user.id,
            refresh_token_hash=hash_refresh_token(refresh_token),
            expires_at=expires_at,
        )
        return access_token, refresh_token
