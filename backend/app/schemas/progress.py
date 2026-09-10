import uuid
from datetime import datetime

from pydantic import BaseModel


class StudentSkillProgressRead(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    skill_id: uuid.UUID
    mastery_score: float
    proficiency_level: str | None = None
    last_practiced_at: datetime | None = None
    updated_at: datetime

    class Config:
        from_attributes = True
