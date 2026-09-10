"""
SQLAlchemy engine + session factory.
Import `get_db` as a FastAPI dependency to get a request-scoped DB session.

NOTE: uses SQLModel's Session (not sqlalchemy.orm.Session) because the rest
of the codebase calls db.exec(select(...)) - SQLModel's Session.exec() is
what supports that syntax. A plain SQLAlchemy Session only has .execute(),
not .exec(), which is exactly what caused the AttributeError.
"""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlmodel import Session

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)


def get_db() -> Generator:
    with Session(engine) as db:
        yield db
