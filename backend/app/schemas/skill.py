import uuid
from datetime import datetime

from pydantic import BaseModel


class SkillRead(BaseModel):
    id: uuid.UUID
    sport_id: uuid.UUID
    parent_skill_id: uuid.UUID | None = None
    name: str
    description: str | None = None
    skill_level: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
