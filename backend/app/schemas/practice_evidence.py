import uuid
from datetime import datetime

from pydantic import BaseModel


class PracticeEvidenceRead(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    training_assignment_id: uuid.UUID
    video_url: str | None = None
    cloudinary_public_id: str | None = None
    submitted_at: datetime
    coach_feedback: str | None = None
    reviewed_at: datetime | None = None

    class Config:
        from_attributes = True


class PracticeEvidenceCreate(BaseModel):
    training_assignment_id: uuid.UUID
    video_url: str | None = None
    cloudinary_public_id: str | None = None
