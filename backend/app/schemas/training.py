import uuid
from datetime import date, datetime

from pydantic import BaseModel

from app.models.training_assignment import AssignmentStatus
from app.models.training_plan import TrainingPlanSourceType, TrainingPlanStatus


class TrainingPlanRead(BaseModel):
    id: uuid.UUID
    student_id: uuid.UUID
    sport_id: uuid.UUID
    source_type: TrainingPlanSourceType
    title: str
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: TrainingPlanStatus
    created_at: datetime

    class Config:
        from_attributes = True


class TrainingAssignmentRead(BaseModel):
    id: uuid.UUID
    training_plan_id: uuid.UUID
    student_id: uuid.UUID
    day_number: int | None = None
    scheduled_date: date | None = None
    drill_id: uuid.UUID
    sets: int | None = None
    reps: int | None = None
    status: AssignmentStatus
    notes: str | None = None

    class Config:
        from_attributes = True


class TrainingAssignmentUpdate(BaseModel):
    status: AssignmentStatus | None = None
    notes: str | None = None
