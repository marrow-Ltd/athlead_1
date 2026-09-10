"""
Skills form a hierarchical tree per sport (skill -> subskills) via
self-referencing parent_skill_id, e.g. Cricket -> Batting -> Stance.
"""
import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Skill(SQLModel, table=True):
    __tablename__ = "skills"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sport_id: uuid.UUID = Field(foreign_key="sports.id", index=True)
    parent_skill_id: uuid.UUID | None = Field(default=None, foreign_key="skills.id", index=True)
    name: str
    description: str | None = None
    skill_level: str | None = None  # e.g. beginner / intermediate / advanced
    prerequisites: str | None = None  # free-text or comma-separated skill ids for MVP
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
