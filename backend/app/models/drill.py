"""
Drills belong to a sport/skill. System drills (is_custom=False) are shared;
coach-created drills (is_custom=True) are private to that coach's students.
"""
import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Drill(SQLModel, table=True):
    __tablename__ = "drills"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sport_id: uuid.UUID = Field(foreign_key="sports.id", index=True)
    skill_id: uuid.UUID | None = Field(default=None, foreign_key="skills.id", index=True)
    drill_name: str
    description: str | None = None
    skill_level: str | None = None
    sets: int | None = None
    reps: int | None = None
    duration_minutes: int | None = None
    video_url: str | None = None
    is_custom: bool = Field(default=False, index=True)
    created_by_coach_id: uuid.UUID | None = Field(default=None, foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
