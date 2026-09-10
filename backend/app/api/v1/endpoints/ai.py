"""
AI/RAG endpoints. Kept intentionally thin for the MVP boilerplate —
each route delegates to ai_recommendation_service, which is the seam
where pgvector-based semantic search / plan generation will plug in.
"""
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.ai import AiRecommendationRequest, AiTrainingPlanRequest, DrillSearchQuery

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/recommendations")
def get_recommendations(
    payload: AiRecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: wire to ai_recommendation_service once embeddings are populated.
    return {"student_id": str(payload.student_id), "recommendations": []}


@router.post("/training-plan")
def generate_training_plan(
    payload: AiTrainingPlanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # TODO: RAG-based plan generation using StudentSkillProgress + drill embeddings.
    return {"student_id": str(payload.student_id), "plan": None, "detail": "Not yet implemented."}


@router.get("/drill-search")
def drill_search(q: str, db: Session = Depends(get_db)):
    # TODO: embed `q` and run a pgvector cosine-distance query against drill_embeddings.
    return {"query": q, "results": []}
