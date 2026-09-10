"""A structured training program for one student, for one sport."""
import uuid
from datetime import date, datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class TrainingPlanSourceType(str, Enum):
    system = "system"
    ai = "ai"
    coach = "coach"


class TrainingPlanStatus(str, Enum):
    active = "active"
    completed = "completed"
    archived = "archived"


class TrainingPlan(SQLModel, table=True):
    __tablename__ = "training_plans"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    student_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    sport_id: uuid.UUID = Field(foreign_key="sports.id", index=True)
    created_by: uuid.UUID | None = Field(default=None, foreign_key="users.id")
    source_type: TrainingPlanSourceType = Field(default=TrainingPlanSourceType.system)
    title: str
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: TrainingPlanStatus = Field(default=TrainingPlanStatus.active)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
