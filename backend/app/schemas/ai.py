import uuid

from pydantic import BaseModel


class DrillSearchQuery(BaseModel):
    query: str
    sport_id: uuid.UUID | None = None
    limit: int = 10


class AiRecommendationRequest(BaseModel):
    student_id: uuid.UUID


class AiTrainingPlanRequest(BaseModel):
    student_id: uuid.UUID
    sport_id: uuid.UUID
    goal: str | None = None
