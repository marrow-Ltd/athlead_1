"""Student-submitted proof of practice (video etc.) plus coach feedback."""
import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class PracticeEvidence(SQLModel, table=True):
    __tablename__ = "practice_evidence"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    student_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    training_assignment_id: uuid.UUID = Field(foreign_key="training_assignments.id", index=True)
    video_url: str | None = None
    cloudinary_public_id: str | None = None
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    coach_feedback: str | None = None
    reviewed_at: datetime | None = None
