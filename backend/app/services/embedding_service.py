"""
Generates and queries pgvector embeddings for drills/skills.
Embedding-model calls are stubbed here — plug in your provider of choice
(OpenAI, Voyage, etc.) behind `embed_text`.
"""
from sqlmodel import Session, select
from sqlalchemy import func

from app.models.embedding import DrillEmbedding, EMBEDDING_DIM


def embed_text(text: str) -> list[float]:
    """Stub — replace with a real embedding-model API call."""
    raise NotImplementedError("Wire this up to your embedding provider.")


def upsert_drill_embedding(db: Session, drill_id, source_text: str) -> DrillEmbedding:
    vector = embed_text(source_text)
    existing = db.exec(select(DrillEmbedding).where(DrillEmbedding.drill_id == drill_id)).first()
    if existing:
        existing.embedding = vector
        existing.source_text = source_text
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing

    row = DrillEmbedding(drill_id=drill_id, embedding=vector, source_text=source_text)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def find_similar_drills(db: Session, query_text: str, limit: int = 10) -> list[DrillEmbedding]:
    query_vector = embed_text(query_text)
    stmt = (
        select(DrillEmbedding)
        .order_by(DrillEmbedding.embedding.cosine_distance(query_vector))
        .limit(limit)
    )
    return db.exec(stmt).all()
