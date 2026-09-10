"""
One-time local setup helper: enables the pgvector extension and can seed
minimal reference data. Run with `python -m app.db.init_db`.
In production this is normally handled by an Alembic migration instead.
"""
from sqlalchemy import text

from app.db.session import engine


def enable_pgvector() -> None:
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()


if __name__ == "__main__":
    enable_pgvector()
    print("pgvector extension enabled.")
