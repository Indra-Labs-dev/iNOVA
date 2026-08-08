"""Auth endpoints — register/login/refresh/logout/me, per
docs/adr/0010-authentication-approach.md. Email verification and MFA are
[PLANNED], not part of Phase 0.
"""
from fastapi import APIRouter, Depends

from app.api.deps import get_auth_service, get_current_user
from app.core.errors import APIError
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse
from app.services.auth_service import AuthError, AuthService

router = APIRouter()


@router.post("/register", status_code=201)
def register(payload: RegisterRequest, service: AuthService = Depends(get_auth_service)) -> dict:
    try:
        user = service.register(email=payload.email, password=payload.password)
    except AuthError as exc:
        raise APIError(409, "email_already_registered", str(exc)) from exc
    return {"id": str(user.id), "email": user.email}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    try:
        access_token, refresh_token = service.login(email=payload.email, password=payload.password)
    except AuthError as exc:
        raise APIError(401, "invalid_credentials", str(exc)) from exc
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    try:
        access_token, refresh_token = service.refresh(payload.refresh_token)
    except AuthError as exc:
        raise APIError(401, "invalid_refresh_token", str(exc)) from exc
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout", status_code=204)
def logout(payload: RefreshRequest, service: AuthService = Depends(get_auth_service)) -> None:
    service.logout(payload.refresh_token)


@router.get("/me")
def me(current_user: User = Depends(get_current_user)) -> dict:
    """Protected route proving the access-token flow end to end."""
    return {"id": str(current_user.id), "email": current_user.email}
