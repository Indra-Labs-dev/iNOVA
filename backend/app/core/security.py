"""Password hashing and JWT helpers.

Implements the mechanism decided in docs/adr/0010-authentication-approach.md:
Argon2id password hashing, short-lived JWT access tokens, opaque rotating
refresh tokens (hashed at rest, see app/models/session.py).
"""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import get_settings

settings = get_settings()
_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False


def create_access_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
        "type": "access",
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    """Raises jwt.PyJWTError on invalid/expired tokens — callers must handle it."""
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


def generate_refresh_token() -> str:
    """Opaque, high-entropy (384-bit) refresh token — never a JWT (avoids leaking claims)."""
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    """SHA-256, not Argon2: the token is already high-entropy and random (unlike a
    password), so a fast, indexable hash is the correct tool here — it lets the
    repository look a session up by hash directly (`WHERE refresh_token_hash = ?`),
    which Argon2's per-call random salt would make impossible."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_refresh_token(token: str, token_hash: str) -> bool:
    return hmac.compare_digest(hash_refresh_token(token), token_hash)
