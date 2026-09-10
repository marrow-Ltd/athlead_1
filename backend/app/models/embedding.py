"""
pgvector-backed embedding tables for semantic search / RAG.
Kept as separate tables (rather than columns on Drill/Skill) so the
vector index can be tuned independently and embeddings can be
regenerated without touching core relational rows.

Uses a 1536-dim vector to match common embedding models (e.g.
OpenAI text-embedding-3-small / Voyage). Adjust the dimension to
whatever embedding model you standardize on.
"""
import uuid
from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlmodel import Field, SQLModel
from sqlalchemy import Column

EMBEDDING_DIM = 1536


class DrillEmbedding(SQLModel, table=True):
    __tablename__ = "drill_embeddings"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    drill_id: uuid.UUID = Field(foreign_key="drills.id", index=True, unique=True)
    embedding: list[float] = Field(sa_column=Column(Vector(EMBEDDING_DIM)))
    source_text: str  # the text that was embedded, kept for debugging/re-embedding
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class SkillEmbedding(SQLModel, table=True):
    __tablename__ = "skill_embeddings"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    skill_id: uuid.UUID = Field(foreign_key="skills.id", index=True, unique=True)
    embedding: list[float] = Field(sa_column=Column(Vector(EMBEDDING_DIM)))
    source_text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
