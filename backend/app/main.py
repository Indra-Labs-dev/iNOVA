# iNOVA — Copyright (c) 2026 Archange Elie Yatte (AEY)
"""FastAPI application entrypoint.

See docs/02-architecture/overview.md and docs/09-backend/architecture.md for
where this fits in the overall system.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import PROJECT_NAME, get_settings
from app.core.errors import register_exception_handlers

settings = get_settings()

app = FastAPI(title=f"{PROJECT_NAME} API", version="0.1.0")

# In development, `flutter run -d chrome` / `flutter build web` + a static
# server can land on an arbitrary localhost port — an explicit allowlist is
# impractical here. A regex scoped to localhost/127.0.0.1 is safe for local
# dev only; production must use `settings.cors_origins`' explicit list (see
# docs/12-security/network-security.md).
if settings.environment == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_v1_prefix)
