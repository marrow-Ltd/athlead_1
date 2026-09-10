"""What a student is assigned to practice on a specific day within a plan."""
import uuid
from datetime import date, datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class AssignmentStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    skipped = "skipped"


class TrainingAssignment(SQLModel, table=True):
    __tablename__ = "training_assignments"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    training_plan_id: uuid.UUID = Field(foreign_key="training_plans.id", index=True)
    student_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    day_number: int | None = None
    scheduled_date: date | None = Field(default=None, index=True)
    drill_id: uuid.UUID = Field(foreign_key="drills.id")
    sets: int | None = None
    reps: int | None = None
    status: AssignmentStatus = Field(default=AssignmentStatus.pending, index=True)
    notes: str | None = None
