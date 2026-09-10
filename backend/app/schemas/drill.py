import uuid
from datetime import datetime

from pydantic import BaseModel


class DrillRead(BaseModel):
    id: uuid.UUID
    sport_id: uuid.UUID
    skill_id: uuid.UUID | None = None
    drill_name: str
    description: str | None = None
    skill_level: str | None = None
    sets: int | None = None
    reps: int | None = None
    duration_minutes: int | None = None
    video_url: str | None = None
    is_custom: bool
    created_by_coach_id: uuid.UUID | None = None
    created_at: datetime

    class Config:
        from_attributes = True
