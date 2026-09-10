"""Tracks a student's mastery of a given skill — drives 'what to practice next'."""
import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class StudentSkillProgress(SQLModel, table=True):
    __tablename__ = "student_skill_progress"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    student_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    skill_id: uuid.UUID = Field(foreign_key="skills.id", index=True)
    mastery_score: float = Field(default=0.0)
    proficiency_level: str | None = None
    last_practiced_at: datetime | None = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
