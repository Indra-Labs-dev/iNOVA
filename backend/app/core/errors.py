"""Error envelope — resolves the open decision in docs/09-backend/error-handling.md
for Phase 0: `{ "error": { "code", "message", "details" } }` on every non-2xx
response. See that document for the full options/criteria record.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class APIError(Exception):
    def __init__(self, status_code: int, code: str, message: str, details: dict | None = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


def _error_response(status_code: int, code: str, message: str, details: dict | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message, "details": details}},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Every handler here converges on the same envelope, per
    docs/09-backend/error-handling.md: never mix the custom shape with
    FastAPI's default `{"detail": ...}` — that includes validation errors
    and any plain `HTTPException`, not just our own `APIError`.
    """

    @app.exception_handler(APIError)
    async def handle_api_error(_: Request, exc: APIError) -> JSONResponse:
        return _error_response(exc.status_code, exc.code, exc.message, exc.details)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        return _error_response(422, "validation_error", "Request validation failed.", {"errors": exc.errors()})

    @app.exception_handler(HTTPException)
    async def handle_http_exception(_: Request, exc: HTTPException) -> JSONResponse:
        return _error_response(exc.status_code, "http_error", str(exc.detail))

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, exc: Exception) -> JSONResponse:
        # Never leak internal detail/stack traces (see docs/12-security/secrets.md).
        return _error_response(500, "internal_error", "An unexpected error occurred.")
