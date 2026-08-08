"""SQLAlchemy engine and session management.

Sync SQLAlchemy 2.0 style, per docs/09-backend/architecture.md — kept
synchronous deliberately for Phase 0 simplicity; revisit only if a real
concurrency bottleneck is measured (see docs/00-overview/product-philosophy.md:
don't build for hypothetical future requirements).
"""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models (see docs/10-data/entities.md)."""


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a request-scoped DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
